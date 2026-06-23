from typing import Optional, Tuple

import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin, clone
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.utils.validation import check_is_fitted
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

from utils.app_logging import logger


class TorchMLPClassifier(BaseEstimator, ClassifierMixin):
    """Um classificador MLP baseado em PyTorch com interface compatível com scikit-learn.

    Implementa `fit`, `predict` e `predict_proba` para uso em pipelines do scikit-learn.
    Esta implementação assume classificação binária (0/1).
    """

    def __init__(
        self,
        input_dim: Optional[int] = None,
        hidden_dims: Tuple[int, ...] = (64, 32),
        dropouts: Tuple[float, ...] = (0.3, 0.2),
        lr: float = 1e-3,
        weight_decay: float = 1e-5,
        batch_size: int = 64,
        epochs: int = 100,
        patience: int = 5,
        min_delta: float = 1e-3,
        random_state: Optional[int] = None,
        device: Optional[str] = None,
        verbose: int = 0,
        threshold: float = 0.5,
    ):
        self.input_dim = input_dim
        self.hidden_dims = tuple(hidden_dims)
        self.dropouts = tuple(dropouts)
        self.lr = lr
        self.weight_decay = weight_decay
        self.batch_size = batch_size
        self.epochs = epochs
        self.patience = patience
        self.min_delta = min_delta
        self.random_state = random_state
        self.device = device
        self.verbose = verbose
        self.threshold = threshold

    def _get_device(self):
        if self.device is not None:
            return torch.device(self.device)
        return torch.device("cuda" if torch.cuda.is_available() else "cpu")

    def _prepare_training_data(self, X, y):
        logger.debug("Preparando dados de treinamento: convertendo X e y para arrays NumPy.")
        x_arr = X.toarray() if hasattr(X, "toarray") else np.asarray(X)
        y_arr = np.asarray(y).ravel().astype(np.float32)

        n_samples, n_features = x_arr.shape
        logger.debug(f"Dados preparados com {n_samples} amostras e {n_features} features.")
        self.n_features_in_ = n_features

        if self.input_dim is None:
            self.input_dim = n_features
            logger.debug(f"input_dim inferido como {self.input_dim}.")

        return x_arr, y_arr, n_samples

    def _build_dataloaders(self, x_arr, y_arr, n_samples):
        logger.debug("Convertendo dados para tensores do PyTorch e criando dataset.")
        x_tensor = torch.from_numpy(x_arr).float()
        y_tensor = torch.from_numpy(y_arr).float().view(-1, 1)
        dataset = TensorDataset(x_tensor, y_tensor)

        val_size = max(1, int(0.2 * n_samples))
        train_size = n_samples - val_size
        logger.debug(
            f"Split de treinamento/validação: train_size={train_size}, val_size={val_size}."
        )
        train_set, val_set = torch.utils.data.random_split(dataset, [train_size, val_size])

        train_loader = DataLoader(
            train_set, batch_size=self.batch_size, shuffle=True, num_workers=0
        )
        val_loader = DataLoader(val_set, batch_size=self.batch_size, shuffle=False, num_workers=0)

        return train_loader, val_loader

    def _build_model(self, input_dim: int) -> nn.Module:
        """Constrói a arquitetura MLP do PyTorch.

        Gera uma `nn.Sequential` com camadas lineares intercaladas por ReLU e Dropout,
        terminando em uma única saída (logit) adequada para `BCEWithLogitsLoss`.
        """
        layers = []
        in_dim = int(input_dim)

        # garantir que há um dropout para cada camada oculta
        dropouts = list(self.dropouts)
        if len(dropouts) < len(self.hidden_dims):
            dropouts = dropouts + [0.0] * (len(self.hidden_dims) - len(dropouts))

        for hid_dim, do in zip(self.hidden_dims, dropouts):
            layers.append(nn.Linear(in_dim, hid_dim))
            layers.append(nn.BatchNorm1d(hid_dim))
            layers.append(nn.LeakyReLU(negative_slope=0.01))
            if do and do > 0.0:
                layers.append(nn.Dropout(do))
            in_dim = hid_dim

        # saída única (logit) para BCEWithLogitsLoss
        layers.append(nn.Linear(in_dim, 1))

        return nn.Sequential(*layers)

    def _initialize_training(self, device):
        logger.info(f"Inicializando modelo MLP com input_dim={self.input_dim} no device={device}.")
        self.model_ = self._build_model(self.input_dim)
        self.model_.to(device)
        criterion = nn.BCEWithLogitsLoss()
        optimizer = optim.Adam(
            self.model_.parameters(), lr=self.lr, weight_decay=self.weight_decay
        )
        return criterion, optimizer

    def _step_epoch(self, loader, device, criterion, optimizer=None):
        if optimizer is not None:
            self.model_.train()
        else:
            self.model_.eval()

        total_loss = 0.0
        with torch.set_grad_enabled(optimizer is not None):
            for xb, yb in loader:
                xb = xb.to(device)
                yb = yb.to(device)

                logits = self.model_(xb)
                loss = criterion(logits, yb)

                if optimizer is not None:
                    optimizer.zero_grad()
                    loss.backward()
                    optimizer.step()

                total_loss += loss.item()

        return total_loss / max(1, len(loader))

    def _update_early_stopping(self, avg_val_loss, best_loss, patience_counter, best_state):
        stop_training = False

        if best_loss is None:
            best_loss = avg_val_loss
            best_state = {k: v.cpu().clone() for k, v in self.model_.state_dict().items()}
            patience_counter = 0
        else:
            improvement = best_loss - avg_val_loss
            if improvement < self.min_delta:
                patience_counter += 1
                if patience_counter >= self.patience:
                    stop_training = True
            else:
                best_loss = avg_val_loss
                patience_counter = 0
                best_state = {k: v.cpu().clone() for k, v in self.model_.state_dict().items()}

        return best_loss, patience_counter, best_state, stop_training

    def fit(self, X, y):
        """Treina o modelo com dados `X` (array-like) e rótulos `y` (0/1)."""
        if self.random_state is not None:
            np.random.seed(self.random_state)
            torch.manual_seed(self.random_state)

        x_arr, y_arr, n_samples = self._prepare_training_data(X, y)
        device = self._get_device()

        train_loader, val_loader = self._build_dataloaders(x_arr, y_arr, n_samples)
        criterion, optimizer = self._initialize_training(device)

        best_loss = None
        patience_counter = 0
        best_state = None

        logger.info("Iniciando treinamento do TorchMLPClassifier.")
        for epoch in range(self.epochs):
            logger.debug(f"Iniciando epoch {epoch + 1}/{self.epochs}.")
            avg_train_loss = self._step_epoch(train_loader, device, criterion, optimizer=optimizer)
            avg_val_loss = self._step_epoch(val_loader, device, criterion, optimizer=None)

            if self.verbose:
                logger.info(
                    f"Epoch {epoch + 1}/{self.epochs} | train_loss={avg_train_loss:.4f} | val_loss={avg_val_loss:.4f}"
                )

            best_loss, patience_counter, best_state, stop_training = self._update_early_stopping(
                avg_val_loss, best_loss, patience_counter, best_state
            )
            if stop_training:
                logger.info(f"Early stopping ativado na epoch {epoch + 1}.")
                break

        if best_state is not None:
            self.model_.load_state_dict(best_state)

        self.model_.to(torch.device("cpu"))
        self.classes_ = np.unique(np.asarray(y))
        self.n_features_in_ = x_arr.shape[1]
        self.is_fitted_ = True
        logger.info(f"Treinamento concluído. Modelo ajustado com {len(self.classes_)} classes.")

        return self

    def cross_validate(
        self,
        X,
        y,
        cv: int = 5,
        scoring="accuracy",
        return_train_score: bool = False,
        n_jobs: int = 1,
        refit: bool = False,
    ) -> dict:
        """Executa validação cruzada usando o mesmo classificador sklearn-compatible.

        O método utiliza `StratifiedKFold` para preservar a proporção das classes em cada fold.
        Se `refit=True`, o estimador atual é treinado novamente com todo o conjunto após a validação.
        """
        cv_splitter = StratifiedKFold(
            n_splits=cv,
            shuffle=True,
            random_state=self.random_state,
        )

        result = cross_validate(
            clone(self),
            X,
            y,
            scoring=scoring,
            cv=cv_splitter,
            return_train_score=return_train_score,
            n_jobs=n_jobs,
            error_score=np.nan,
        )

        if refit:
            self.fit(X, y)

        return result

    def predict_proba(self, X):
        check_is_fitted(self, "is_fitted_")
        x_arr = X.toarray() if hasattr(X, "toarray") else np.asarray(X)
        device = next(self.model_.parameters()).device
        logger.debug("Gerando probabilidades no método predict_proba.")
        self.model_.eval()
        x_tensor = torch.from_numpy(x_arr).float().to(device)
        with torch.no_grad():
            logits = self.model_(x_tensor)
            probs = torch.sigmoid(logits).cpu().numpy().flatten()

        # retornar formato (n_samples, n_classes)
        proba = np.vstack([1 - probs, probs]).T
        return proba

    def predict(self, X):
        proba = self.predict_proba(X)
        preds = (proba[:, 1] >= self.threshold).astype(int)
        # mapear para valores originais de classes_ se necessário
        if hasattr(self, "classes_"):
            return self.classes_[preds]
        return preds


__all__ = ["TorchMLPClassifier"]
