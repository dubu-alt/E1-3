# ============================================================================
# 1. 2차원 배열 데이터 구조 및 MAC 연산
# ============================================================================

class Matrix:
    """n×n 2차원 배열을 저장하고 접근하는 클래스"""
    
    def __init__(self, data: List[List[float]]):
        """
        Args:
            data: 2차원 리스트 (모두 같은 행 길이)
        """
        self.data = data
        self.size = len(data)  # n×n의 n
        
        # 검증: 모든 행의 길이가 같은지 확인
        if not all(len(row) == self.size for row in data):
            raise ValueError(f"모든 행의 길이가 {self.size}이어야 합니다.")
    
    def get(self, i: int, j: int) -> float:
        """위치 (i, j)의 값 반환"""
        return self.data[i][j]
    
    def set(self, i: int, j: int, value: float) -> None:
        """위치 (i, j)에 값 설정"""
        self.data[i][j] = value
    
    def __repr__(self) -> str:
        return f"Matrix({self.size}×{self.size})"
    
def compute_mac(filter_matrix: Matrix, pattern_matrix: Matrix) -> float:
    """
    MAC(Multiply-Accumulate) 연산 수행
    필터와 패턴을 겹쳐서 같은 위치끼리 곱하고, 결과를 모두 더함
    
    Args:
        filter_matrix: 필터 (Matrix 객체)
        pattern_matrix: 패턴 (Matrix 객체)
    
    Returns:
        점수 (float)
    
    Raises:
        ValueError: 두 행렬의 크기가 다르면 예외 발생
    """
    if filter_matrix.size != pattern_matrix.size:
        raise ValueError(
            f"크기 불일치: 필터 {filter_matrix.size}×{filter_matrix.size}, "
            f"패턴 {pattern_matrix.size}×{pattern_matrix.size}"
        )
    
    score = 0.0
    n = filter_matrix.size
    
    # 반복문으로 직접 구현
    for i in range(n):
        for j in range(n):
            score += filter_matrix.get(i, j) * pattern_matrix.get(i, j)
    
    return score

# ============================================================================
# 2. 라벨 정규화 (Label Normalization)
# ============================================================================

def normalize_label(label: str) -> str:
    """
    라벨을 표준 형식으로 정규화
    '+' → 'Cross', 'x' → 'X', 'cross' → 'Cross', 등
    
    Args:
        label: 원본 라벨 (문자열)
    
    Returns:
        정규화된 라벨 ('Cross' 또는 'X')
    
    Raises:
        ValueError: 인식 불가능한 라벨
    """
    label = str(label).strip().lower()
    
    if label in ('+', 'cross'):
        return 'Cross'
    elif label in ('x',):
        return 'X'
    else:
        raise ValueError(f"인식 불가능한 라벨: {label}")

# ============================================================================
# 3. 점수 비교 및 판정 (Epsilon 기반)
# ============================================================================

EPSILON = 1e-9

def judge_scores(score_a: float, score_b: float) -> str:
    """
    두 점수를 비교하여 판정 결과 반환
    
    Args:
        score_a: A 필터의 점수
        score_b: B 필터의 점수
    
    Returns:
        'A', 'B', 또는 'UNDECIDED'
    """
    diff = abs(score_a - score_b)
    
    if diff < EPSILON:
        return 'UNDECIDED'
    elif score_a > score_b:
        return 'A'
    else:
        return 'B'


def label_from_judgment(result: str) -> Optional[str]:
    """
    판정 결과를 라벨로 변환
    
    Args:
        result: 'A', 'B', 또는 'UNDECIDED'
    
    Returns:
        'Cross', 'X', 또는 None (UNDECIDED인 경우)
    """
    # 가정: A = Cross, B = X
    label_map = {'A': 'Cross', 'B': 'X'}
    return label_map.get(result)

# ============================================================================
# 6. 모드 1: 사용자 입력 (3×3)
# ============================================================================

def mode_user_input():
    """모드 1: 사용자가 직접 입력하는 3×3 필터/패턴 분석"""
    print("\n" + "=" * 50)
    print("# [모드 1] 사용자 입력 (3×3)")
    print("=" * 50)
    
    # 필터 A, B 입력
    print("\n#---------------------------------------")
    print("# [1] 필터 입력")
    print("#---------------------------------------")
    
    filter_a = read_matrix_from_console("필터 A (3줄 입력, 공백 구분):", 3)
    if not filter_a:
        return
    
    filter_b = read_matrix_from_console("필터 B (3줄 입력, 공백 구분):", 3)
    if not filter_b:
        return
    
    # 패턴 입력
    print("\n#---------------------------------------")
    print("# [2] 패턴 입력")
    print("#---------------------------------------")
    
    pattern = read_matrix_from_console("패턴 (3줄 입력, 공백 구분):", 3)
    if not pattern:
        return
    
    # MAC 연산
    print("\n#---------------------------------------")
    print("# [3] MAC 결과")
    print("#---------------------------------------")
    
    try:
        score_a = compute_mac(filter_a, pattern)
        score_b = compute_mac(filter_b, pattern)
        avg_time = measure_mac_time(filter_a, pattern, iterations=10)
        
        print(f"A 점수: {score_a}")
        print(f"B 점수: {score_b}")
        print(f"연산 시간(평균/10회): {avg_time:.6f} ms")
        
        result = judge_scores(score_a, score_b)
        if result == 'UNDECIDED':
            print(f"판정: 판정 불가 (|A-B| = {abs(score_a - score_b):.2e} < {EPSILON})")
        else:
            print(f"판정: {result}")
    
    except Exception as e:
        print(f"오류: {e}")