# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the LICENSE file in
# the root directory of this source tree. An additional grant of patent rights
# can be found in the PATENTS file in the same directory.

from fairseq import checkpoint_utils
from fairseq.models import (
    register_model,
    register_model_architecture,
)
from fairseq.models.speech_to_text import (
    ConvTransformerModel,
    convtransformer_espnet,
    ConvTransformerEncoder,
)
from fairseq.models.speech_to_text.modules.augmented_memory_attention import (
    augmented_memory,
    SequenceEncoder,
    AugmentedMemoryConvTransformerEncoder,
)
from fairseq.models.speech_to_text.modules.augmented_memory_attention_layer_mem import (
    augmented_memory_layer_mem,
    SequenceEncoder_layer_mem,
    AugmentedMemoryConvTransformerEncoder_layer_mem,
)
from fairseq.models.speech_to_text.modules.augmented_memory_attention_enc_mem import (
    augmented_memory_enc_mem,
    SequenceEncoder_enc_mem,
    AugmentedMemoryConvTransformerEncoder_enc_mem,
)
from fairseq.models.speech_to_text.modules.augmented_memory_attention_query_size import (
    augmented_memory_query_size,
    SequenceEncoder_query_size,
    AugmentedMemoryConvTransformerEncoder_query_size,
)
from fairseq.models.speech_to_text.modules.augmented_memory_attention_no_sum import (
    augmented_memory_no_sum,
    SequenceEncoder_no_sum,
    AugmentedMemoryConvTransformerEncoder_no_sum,
)

from torch import nn, Tensor
from typing import Dict, List
from fairseq.models.speech_to_text.modules.emformer import NoSegAugmentedMemoryTransformerEncoderLayer

@register_model("convtransformer_simul_trans")
class SimulConvTransformerModel(ConvTransformerModel):
    """
    Implementation of the paper:

    SimulMT to SimulST: Adapting Simultaneous Text Translation to
    End-to-End Simultaneous Speech Translation

    https://www.aclweb.org/anthology/2020.aacl-main.58.pdf
    """

    @staticmethod
    def add_args(parser):
        super(SimulConvTransformerModel, SimulConvTransformerModel).add_args(parser)
        parser.add_argument(
            "--train-monotonic-only",
            action="store_true",
            default=False,
            help="Only train monotonic attention",
        )
        parser.add_argument( # DP
            "--encoder-mask-future-delay",
            type=int,
            metavar="N",
            help="Specify degree of attention into future when using encoder attention masking. Default=infinite (full attention)",
        )
        parser.add_argument( # DP
            "--encoder-mask-block-size",
            type=int,
            metavar="N",
            help="Specify size of input blocks for which block attention is allowed. Useful when inputs will be grouped following encoder (e.g., simultaneous translation using wait-k). Default=1 (no additional attention)",
        )

    @classmethod
    def build_decoder(cls, args, task, embed_tokens):
        tgt_dict = task.tgt_dict

        from examples.simultaneous_translation.models.transformer_monotonic_attention import (
            TransformerMonotonicDecoder,
        )

        decoder = TransformerMonotonicDecoder(args, tgt_dict, embed_tokens)

        if getattr(args, "load_pretrained_decoder_from", None):
            decoder = checkpoint_utils.load_pretrained_component_from_model(
                component=decoder, checkpoint=args.load_pretrained_decoder_from
            )
        return decoder


@register_model_architecture(
    "convtransformer_simul_trans", "convtransformer_simul_trans_espnet"
)
def convtransformer_simul_trans_espnet(args):
    convtransformer_espnet(args)

#Default Augmented Memory Transormer
@register_model("convtransformer_augmented_memory")
@augmented_memory
class AugmentedMemoryConvTransformerModel(SimulConvTransformerModel):
    @classmethod
    def build_encoder(cls, args):
        encoder = SequenceEncoder(args, AugmentedMemoryConvTransformerEncoder(args))

        if getattr(args, "load_pretrained_encoder_from", None) is not None:
            encoder = checkpoint_utils.load_pretrained_component_from_model(
                component=encoder, checkpoint=args.load_pretrained_encoder_from
            )

        return encoder


@register_model_architecture(
    "convtransformer_augmented_memory", "convtransformer_augmented_memory"
)
def augmented_memory_convtransformer_espnet(args):
    convtransformer_espnet(args)

#Layer_Mem Augment Memory Transformer
@register_model("convtransformer_augmented_memory_layer_mem")
@augmented_memory_layer_mem
class AugmentedMemoryConvTransformerModel_layer_mem(SimulConvTransformerModel):
    @classmethod
    def build_encoder(cls, args):
        encoder = SequenceEncoder_layer_mem(args, AugmentedMemoryConvTransformerEncoder_layer_mem(args))

        if getattr(args, "load_pretrained_encoder_from", None) is not None:
            encoder = checkpoint_utils.load_pretrained_component_from_model(
                component=encoder, checkpoint=args.load_pretrained_encoder_from
            )

        return encoder


@register_model_architecture(
    "convtransformer_augmented_memory_layer_mem", "convtransformer_augmented_memory_layer_mem"
)
def augmented_memory_layer_mem_convtransformer_espnet(args):
    convtransformer_espnet(args)

#Enc_Mem Augmented Memory Transormer
@register_model("convtransformer_augmented_memory_enc_mem")
@augmented_memory_enc_mem
class AugmentedMemoryConvTransformerModel_enc_mem(SimulConvTransformerModel):
    @classmethod
    def build_encoder(cls, args):
        encoder = SequenceEncoder_enc_mem(args, AugmentedMemoryConvTransformerEncoder_enc_mem(args))

        if getattr(args, "load_pretrained_encoder_from", None) is not None:
            encoder = checkpoint_utils.load_pretrained_component_from_model(
                component=encoder, checkpoint=args.load_pretrained_encoder_from
            )

        return encoder


@register_model_architecture(
    "convtransformer_augmented_memory_enc_mem", "convtransformer_augmented_memory_enc_mem"
)
def augmented_memory_enc_mem_convtransformer_espnet(args):
    convtransformer_espnet(args)

#Query_Size Augmented Memory Transormer
@register_model("convtransformer_augmented_memory_query_size")
@augmented_memory_query_size
class AugmentedMemoryConvTransformerModel_query_size(SimulConvTransformerModel):
    @classmethod
    def build_encoder(cls, args):
        encoder = SequenceEncoder_query_size(args, AugmentedMemoryConvTransformerEncoder_query_size(args))

        if getattr(args, "load_pretrained_encoder_from", None) is not None:
            encoder = checkpoint_utils.load_pretrained_component_from_model(
                component=encoder, checkpoint=args.load_pretrained_encoder_from
            )

        return encoder


@register_model_architecture(
    "convtransformer_augmented_memory_query_size", "convtransformer_augmented_memory_query_size"
)
def augmented_memory_query_size_convtransformer_espnet(args):
    convtransformer_espnet(args)

#No_Sum Augmented Memory Transormer
@register_model("convtransformer_augmented_memory_no_sum")
@augmented_memory_no_sum
class AugmentedMemoryConvTransformerModel_no_sum(SimulConvTransformerModel):
    @classmethod
    def build_encoder(cls, args):
        encoder = SequenceEncoder_no_sum(args, AugmentedMemoryConvTransformerEncoder_no_sum(args))

        if getattr(args, "load_pretrained_encoder_from", None) is not None:
            encoder = checkpoint_utils.load_pretrained_component_from_model(
                component=encoder, checkpoint=args.load_pretrained_encoder_from
            )

        return encoder


@register_model_architecture(
    "convtransformer_augmented_memory_no_sum", "convtransformer_augmented_memory_no_sum"
)
def augmented_memory_no_sum_convtransformer_espnet(args):
    convtransformer_espnet(args)

# ============================================================================ #
#   Convtransformer
#   with monotonic attention decoder
#   with emformer encoder
# ============================================================================ #


class ConvTransformerEmformerEncoder(ConvTransformerEncoder):
    def __init__(self, args):
        super().__init__(args)
        stride = self.conv_layer_stride(args)
        trf_left_context = args.segment_left_context // stride
        trf_right_context = args.segment_right_context // stride
        context_config = [trf_left_context, trf_right_context]
        self.transformer_layers = nn.ModuleList(
            [
                NoSegAugmentedMemoryTransformerEncoderLayer(
                    input_dim=args.encoder_embed_dim,
                    num_heads=args.encoder_attention_heads,
                    ffn_dim=args.encoder_ffn_embed_dim,
                    num_layers=args.encoder_layers,
                    dropout_in_attn=args.dropout,
                    dropout_on_attn=args.dropout,
                    dropout_on_fc1=args.dropout,
                    dropout_on_fc2=args.dropout,
                    activation_fn=args.activation_fn,
                    context_config=context_config,
                    segment_size=args.segment_length,
                    max_memory_size=args.max_memory_size,
                    scaled_init=True,  # TODO: use constant for now.
                    tanh_on_mem=args.amtrf_tanh_on_mem,
                )
            ]
        )
        self.conv_transformer_encoder = ConvTransformerEncoder(args)

    def forward(self, src_tokens, src_lengths):
        encoder_out: Dict[str, List[Tensor]] = self.conv_transformer_encoder(src_tokens, src_lengths.to(src_tokens.device))
        output = encoder_out["encoder_out"][0]
        encoder_padding_masks = encoder_out["encoder_padding_mask"]

        return {
            "encoder_out": [output],
            # This is because that in the original implementation
            # the output didn't consider the last segment as right context.
            "encoder_padding_mask": [encoder_padding_masks[0][:, : output.size(0)]] if len(encoder_padding_masks) > 0
            else [],
            "encoder_embedding": [],
            "encoder_states": [],
            "src_tokens": [],
            "src_lengths": [],
        }

    @staticmethod
    def conv_layer_stride(args):
        # TODO: make it configurable from the args
        return 4


@register_model("convtransformer_emformer")
class ConvtransformerEmformer(SimulConvTransformerModel):
    @staticmethod
    def add_args(parser):
        super(ConvtransformerEmformer, ConvtransformerEmformer).add_args(parser)

        parser.add_argument(
            "--segment-length",
            type=int,
            metavar="N",
            help="length of each segment (not including left context / right context)",
        )
        parser.add_argument(
            "--segment-left-context",
            type=int,
            help="length of left context in a segment",
        )
        parser.add_argument(
            "--segment-right-context",
            type=int,
            help="length of right context in a segment",
        )
        parser.add_argument(
            "--max-memory-size",
            type=int,
            default=-1,
            help="Right context for the segment.",
        )
        parser.add_argument(
            "--amtrf-tanh-on-mem",
            default=False,
            action="store_true",
            help="whether to use tanh on memory vector",
        )

    @classmethod
    def build_encoder(cls, args):
        encoder = ConvTransformerEmformerEncoder(args)
        if getattr(args, "load_pretrained_encoder_from", None):
            encoder = checkpoint_utils.load_pretrained_component_from_model(
                component=encoder, checkpoint=args.load_pretrained_encoder_from
            )
        return encoder


@register_model_architecture(
    "convtransformer_emformer",
    "convtransformer_emformer",
)
def convtransformer_emformer_base(args):
    convtransformer_espnet(args)
