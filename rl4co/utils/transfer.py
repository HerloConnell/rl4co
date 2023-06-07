import torch.nn as nn


def transplant_weights(
    source: nn.Module, target: nn.Module, load_encoder: bool = True, load_decoder: bool = True
):
    source_policy = source.model.policy
    target_policy = target.model.policy

    # Transplant encoder's params except init_embedding
    if load_encoder:
        source_encoder_params = source_policy.encoder.layers.state_dict()
        target_policy.encoder.layers.load_state_dict(source_encoder_params)

    # Transplant decoder params context and dynamic embedding
    if load_decoder:
        source_decoder = source_policy.decoder
        target_decoder = target_policy.decoder
        iter_ = zip(source_decoder.named_children(), target_decoder.named_children())

        for (name, source), (_, target) in iter_:
            if name in ["env", "context", "dynamic_embedding"]:
                continue

            target.load_state_dict(source.state_dict())
