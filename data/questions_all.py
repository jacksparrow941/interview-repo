"""
Master question aggregator.
Imports all question modules and combines into ALL_QUESTIONS.
Full HTML answers override short hints for legacy questions.
"""
from data.questions_coding import QUESTIONS as _CODING
from data.questions_lld import LLD_Q, BEHAVIORAL_Q
from data.questions_full_answers import FULL_ANSWERS

# Extended question banks (full HTML answers)
from data.questions_cicd    import QUESTIONS as _CICD
from data.questions_cpp_ext  import QUESTIONS as _CPP_EXT
from data.questions_cpp_ext2 import QUESTIONS as _CPP_EXT2
from data.questions_java_ext  import QUESTIONS as _JAVA_EXT
from data.questions_java_ext2 import QUESTIONS as _JAVA_EXT2
from data.questions_go_ext   import QUESTIONS as _GO_EXT
from data.questions_go_ext2  import QUESTIONS as _GO_EXT2
from data.questions_db_ext   import QUESTIONS as _DB_EXT
from data.questions_net_ext  import QUESTIONS as _NET_EXT
from data.questions_os_ext   import QUESTIONS as _OS_EXT
from data.questions_lld_ext  import QUESTIONS as _LLD_EXT
from data.questions_sd_ext   import QUESTIONS as _SD_EXT
from data.questions_security import QUESTIONS as _SECURITY
from data.questions_mlsys    import QUESTIONS as _MLSYS
from data.questions_perf     import QUESTIONS as _PERF
from data.questions_mufg     import QUESTIONS as _MUFG
from data.questions_mufg2    import QUESTIONS as _MUFG2
from data.questions_mufg3    import QUESTIONS as _MUFG3

# Legacy base questions (raw tuples from questions_other.py)
from data.questions_other import (
    BACKEND_QUESTIONS, CPP_QUESTIONS, JAVA_QUESTIONS, GO_QUESTIONS,
    SYSDESIGN_QUESTIONS, DB_QUESTIONS, OS_QUESTIONS, NET_QUESTIONS, CONC_QUESTIONS
)

def _to_dict(q):
    return {
        "id": q[0], "text": q[1], "category": q[2], "subcategory": q[3],
        "difficulty": q[4], "companies": q[5], "frequency": q[6],
        "tags": q[7].split(","), "round_type": q[8], "answer_hint": q[9]
    }

def _enrich(q):
    """Apply full HTML answer override if available for this question ID."""
    qid = q.get("id", "")
    if qid in FULL_ANSWERS:
        q = dict(q)
        q["answer_hint"] = FULL_ANSWERS[qid]
    return q

_OTHER = [_to_dict(q) for q in (
    BACKEND_QUESTIONS + CPP_QUESTIONS + JAVA_QUESTIONS + GO_QUESTIONS +
    SYSDESIGN_QUESTIONS + DB_QUESTIONS + OS_QUESTIONS + NET_QUESTIONS + CONC_QUESTIONS
)]

_RAW = (
    _CODING +       # 80 DSA
    _OTHER +        # 121 base (backend/cpp/java/go/sd/db/os/net/concurrency)
    LLD_Q +         # 25 LLD
    BEHAVIORAL_Q +  # 10 behavioral
    _CICD +         # 20 CI/CD
    _CPP_EXT +      # 12 C++ extended
    _CPP_EXT2 +     # 11 C++ extended part 2
    _JAVA_EXT +     # 10 Java extended
    _JAVA_EXT2 +    # 10 Java extended part 2
    _GO_EXT +       # 10 Go extended
    _GO_EXT2 +      # 8 Go extended part 2
    _DB_EXT +       # 12 Database extended
    _NET_EXT +      # 11 Networking extended
    _OS_EXT +       # 10 OS extended
    _LLD_EXT +      # 7 LLD extended
    _SD_EXT +       # 8 System Design extended
    _SECURITY +     # 8 Security questions
    _MLSYS +        # 8 ML Systems questions
    _PERF +         # 6 Performance & Observability questions
    _MUFG +         # 20 MUFG Global Services (core Java + banking)
    _MUFG2 +         # 11 MUFG JD-specific (React, Redux, JS, testing, SAML, AWS)
    _MUFG3          # 12 MUFG ByteByteGo deep-dives (system_design, concurrency, coding, DB, security)
)

# Apply full HTML answer overrides to all questions
ALL_QUESTIONS = [_enrich(q) for q in _RAW]
