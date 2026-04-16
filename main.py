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
# 4. 성능 측정
# ============================================================================

def measure_mac_time(filter_matrix: Matrix, pattern_matrix: Matrix, 
                     iterations: int = 10) -> float:
    """
    MAC 연산의 평균 실행 시간 측정 (ms 단위)
    
    Args:
        filter_matrix: 필터
        pattern_matrix: 패턴
        iterations: 반복 측정 횟수 (기본값 10)
    
    Returns:
        평균 실행 시간 (밀리초)
    """
    total_time = 0.0
    
    for _ in range(iterations):
        start = time.time()
        compute_mac(filter_matrix, pattern_matrix)
        end = time.time()
        total_time += (end - start) * 1000  # 초 → 밀리초
    
    return total_time / iterations

# ============================================================================
# 5. 콘솔 입력 처리
# ============================================================================

def read_matrix_from_console(prompt: str, expected_size: int) -> Optional[Matrix]:
    """
    콘솔에서 n×n 행렬을 사용자 입력으로 읽기
    
    Args:
        prompt: 출력할 안내 문구
        expected_size: 기대하는 행렬 크기 (n)
    
    Returns:
        Matrix 객체 또는 None (입력 실패 시)
    """
    print(prompt)
    
    data = []
    for line_num in range(expected_size):
        while True:
            try:
                line = input(f"줄 {line_num + 1}: ")
                values = list(map(float, line.split()))
                
                if len(values) != expected_size:
                    print(f"입력 형식 오류: 정확히 {expected_size}개의 숫자를 공백으로 구분해 입력하세요.")
                    continue
                
                data.append(values)
                break
            
            except ValueError:
                print(f"입력 형식 오류: 각 줄에 {expected_size}개의 숫자를 공백으로 구분해 입력하세요.")
    
    return Matrix(data)

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

# ============================================================================
# 7. 모드 2: JSON 파일 분석
# ============================================================================

def load_json_data(filepath: str) -> Optional[Dict]:
    """
    JSON 파일에서 필터와 패턴 데이터 로드
    
    Args:
        filepath: data.json 파일 경로
    
    Returns:
        파싱된 JSON 딕셔너리 또는 None
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"오류: {filepath} 파일을 찾을 수 없습니다.")
        return None
    except json.JSONDecodeError as e:
        print(f"오류: JSON 형식이 잘못되었습니다. {e}")
        return None


def mode_json_analysis():
    """모드 2: data.json 파일 분석"""
    print("\n" + "=" * 50)
    print("# [모드 2] data.json 분석")
    print("=" * 50)
    
    # JSON 로드
    data = load_json_data('data.json')
    if not data:
        return
    
    # 필터 로드
    print("\n#---------------------------------------")
    print("# [1] 필터 로드")
    print("#---------------------------------------")
    
    filters = {}
    try:
        for size_key in ['size_5', 'size_13', 'size_25']:
            if size_key not in data.get('filters', {}):
                print(f"⚠ {size_key} 필터를 찾을 수 없습니다.")
                continue
            
            filter_data = data['filters'][size_key]
            size = int(size_key.split('_')[1])
            
            # 필터별로 라벨 정규화
            cross_label = None
            x_label = None
            
            for key in filter_data.keys():
                normalized = normalize_label(key)
                if normalized == 'Cross':
                    cross_label = key
                elif normalized == 'X':
                    x_label = key
            
            if cross_label and x_label:
                filters[size_key] = {
                    'size': size,
                    'cross': Matrix(filter_data[cross_label]),
                    'x': Matrix(filter_data[x_label]),
                    'cross_label': cross_label,
                    'x_label': x_label
                }
                print(f"✓ {size_key} 필터 로드 완료 (Cross, X)")
            else:
                print(f"⚠ {size_key} 필터가 불완전합니다.")
    
    except Exception as e:
        print(f"오류: 필터 로드 중 문제 발생 - {e}")
        return
    
    # 패턴 분석
    print("\n#---------------------------------------")
    print("# [2] 패턴 분석 (라벨 정규화 적용)")
    print("#---------------------------------------")
    
    test_results = []
    size_performance = {}  # 크기별 성능 데이터 수집
    
    patterns = data.get('patterns', {})
    for pattern_key in sorted(patterns.keys()):
        pattern_data = patterns[pattern_key]
        
        # 패턴 키에서 크기 추출 (예: size_5_1 → size_5)
        parts = pattern_key.rsplit('_', 1)
        size_key = parts[0] if len(parts) == 2 else pattern_key
        
        if size_key not in filters:
            print(f"\n- -- {pattern_key} ---")
            print(f"⚠ {size_key} 필터를 찾을 수 없습니다. [FAIL]")
            test_results.append((pattern_key, 'FAIL', '필터 누락'))
            continue
        
        try:
            # 패턴 크기 검증
            pattern_list = pattern_data.get('input')
            pattern_size = len(pattern_list)
            expected_size = filters[size_key]['size']
            
            if pattern_size != expected_size:
                print(f"\n- -- {pattern_key} ---")
                print(f"⚠ 크기 불일치: 패턴 {pattern_size}×{pattern_size}, "
                      f"필터 {expected_size}×{expected_size}. [FAIL]")
                test_results.append((pattern_key, 'FAIL', '크기 불일치'))
                continue
            
            # 패턴을 Matrix로 변환
            pattern = Matrix(pattern_list)
            
            # MAC 연산
            filter_cross = filters[size_key]['cross']
            filter_x = filters[size_key]['x']
            
            score_cross = compute_mac(filter_cross, pattern)
            score_x = compute_mac(filter_x, pattern)
            
            # 판정
            result = judge_scores(score_cross, score_x)
            predicted_label = label_from_judgment(result)
            
            # Expected 라벨 정규화
            expected_raw = pattern_data.get('expected', '')
            expected_label = normalize_label(expected_raw)
            
            # PASS/FAIL 판정
            is_pass = predicted_label == expected_label
            pass_fail = 'PASS' if is_pass else 'FAIL'
            
            # 콘솔 출력
            print(f"\n- -- {pattern_key} ---")
            print(f"Cross 점수: {score_cross}")
            print(f"X 점수: {score_x}")
            
            if result == 'UNDECIDED':
                print(f"판정: UNDECIDED | expected: {expected_label} | {pass_fail} (동점 규칙)")
            else:
                print(f"판정: {predicted_label} | expected: {expected_label} | {pass_fail}")
            
            test_results.append((pattern_key, pass_fail, result))
            
            # 성능 데이터 수집
            if expected_size not in size_performance:
                size_performance[expected_size] = []
            
            size_performance[expected_size].append(pattern)
        
        except Exception as e:
            print(f"\n- -- {pattern_key} ---")
            print(f"오류: {e} [FAIL]")
            test_results.append((pattern_key, 'FAIL', str(e)))
    
    # 성능 분석
    print("\n#---------------------------------------")
    print("# [3] 성능 분석 (평균/10회)")
    print("#---------------------------------------")
    print(f"{'크기':<8} {'평균 시간(ms)':<16} {'연산 횟수':<10}")
    print("-" * 40)
    
    for size in sorted(size_performance.keys()):
        if size_performance[size]:
            # 첫 번째 패턴으로 성능 측정
            sample_pattern = size_performance[size][0]
            size_key = f'size_{size}'
            
            if size_key in filters:
                avg_time = measure_mac_time(filters[size_key]['cross'], 
                                            sample_pattern, iterations=10)
                operation_count = size * size
                print(f"{size}×{size:<5} {avg_time:<16.6f} {operation_count:<10}")
    
    # 결과 요약
    print("\n#---------------------------------------")
    print("# [4] 결과 요약")
    print("#---------------------------------------")
    
    total_tests = len(test_results)
    passed_tests = sum(1 for _, status, _ in test_results if status == 'PASS')
    failed_tests = total_tests - passed_tests
    
    print(f"총 테스트: {total_tests}개")
    print(f"통과: {passed_tests}개")
    print(f"실패: {failed_tests}개")
    
    if failed_tests > 0:
        print("\n실패 케이스:")
        for pattern_key, status, reason in test_results:
            if status == 'FAIL':
                print(f"- {pattern_key}: {reason}")

# ============================================================================
# 8. 메인 함수
# ============================================================================

def main():
    """프로그램 메인 함수"""
    print("\n" + "=" * 50)
    print("=== Mini NPU Simulator ===")
    print("=" * 50)
    
    print("\n[모드 선택]\n")
    print("1. 사용자 입력 (3×3)")
    print("2. data.json 분석")
    
    while True:
        choice = input("\n선택: ").strip()
        
        if choice == '1':
            mode_user_input()
            break
        elif choice == '2':
            mode_json_analysis()
            break
        else:
            print("잘못된 선택입니다. 1 또는 2를 입력하세요.")


if __name__ == '__main__':
    main()
