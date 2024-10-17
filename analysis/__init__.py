from analysis.base import Model
from analysis.lda import LDAModel
from analysis.nmf import NMFFrobeniusModel, NMFKullbackLeiblerModel

MODELS = {
    "NMF with Kullback-Leibler": NMFKullbackLeiblerModel,
    "NMF with Frobenius norm": NMFFrobeniusModel,
    "LDA": LDAModel
}


def load_model(kind: str, **kwargs) -> Model:
    if kind not in MODELS:
        raise ValueError(f"Type {kind} not found. Available scrapers: {MODELS.keys()}")
    return MODELS[kind](**kwargs)
