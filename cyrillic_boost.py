import torch
from transformers import LogitsProcessor


class CyrillicBoostLogitsProcessor(LogitsProcessor):
    """
    Добавляет бонус к логитам токенов, содержащих кириллицу.
    Остальные токены не изменяет.
    """

    def __init__(self, tokenizer, boost: float = 4.0):
        self.boost = boost
        self.cyrillic_token_ids = self._get_cyrillic_tokens(tokenizer)

    def _get_cyrillic_tokens(self, tokenizer):
        cyrillic_ids = []
        for token_id in range(tokenizer.vocab_size):
            token = tokenizer.decode([token_id])
            if any("а" <= c <= "я" or "А" <= c <= "Я" or c in "ёЁ" for c in token):
                cyrillic_ids.append(token_id)
        return cyrillic_ids

    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor) -> torch.FloatTensor:
        scores[:, self.cyrillic_token_ids] += self.boost
        return scores
