"""
Master full-answer override map.
Maps question_id → rich HTML answer string.
These override the short hints in the legacy question files.
"""
from data.questions_fa_backend  import FULL_ANSWERS_BACKEND
from data.questions_fa_backend2 import FULL_ANSWERS_BACKEND2
from data.questions_fa_coding   import FULL_ANSWERS_CODING
from data.questions_fa_lld      import FULL_ANSWERS_LLD
from data.questions_fa_lang     import FULL_ANSWERS_LANG
from data.questions_fa_sysdb    import FULL_ANSWERS_SYSDB

FULL_ANSWERS = {
    **FULL_ANSWERS_BACKEND,
    **FULL_ANSWERS_BACKEND2,
    **FULL_ANSWERS_CODING,
    **FULL_ANSWERS_LLD,
    **FULL_ANSWERS_LANG,
    **FULL_ANSWERS_SYSDB,
}
