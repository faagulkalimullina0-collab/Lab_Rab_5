"""Тесты модуля num_series.moving_average (SMA, CMA, EMA, benchmark).""" 
import random 
import pytest 
from num_series.moving_average import ( 
    simple_moving_average, 
    centered_moving_average, 
    exponential_moving_average, 
    benchmark_moving_average, 
) 
  
  
class TestSimpleMovingAverage: 
    def test_window_equals_length(self): 
        assert simple_moving_average([1, 2, 3], 3) == [2.0] 
  
    def test_classic_example(self): 
        assert simple_moving_average([1, 2, 3, 4, 5], 3) == [2.0, 3.0, 4.0] 
  
    def test_window_1_returns_original(self): 
        data = [1.0, 2.5, -3.0, 4.0] 
        assert simple_moving_average(data, 1) == data 
  
    def test_output_length(self): 
        data = list(range(10)) 
        for w in range(1, 11): 
            assert len(simple_moving_average(data, w)) == len(data) - w + 1 
  
    def test_constant_series(self): 
        data = [5.0] * 10 
        assert simple_moving_average(data, 3) == [5.0] * 8 
  
    def test_matches_naive(self): 
        rng = random.Random(0) 
        data = [rng.uniform(-10, 10) for _ in range(50)] 
        w = 7 
        naive = [sum(data[i:i + w]) / w for i in range(len(data) - w + 1)] 
        fast = simple_moving_average(data, w) 
        assert fast == pytest.approx(naive) 
  
    @pytest.mark.parametrize("bad_window", [0, -1, 1.5, True]) 
    def test_invalid_window_raises(self, bad_window): 
        with pytest.raises(ValueError): 
            simple_moving_average([1, 2, 3], bad_window) 
  
    def test_window_bigger_than_data_raises(self): 
        with pytest.raises(ValueError, match="больше длины"): 
            simple_moving_average([1, 2], 5) 
  
    def test_empty_data_raises(self): 
        with pytest.raises(ValueError): 
            simple_moving_average([], 1)
  
class TestCenteredMovingAverage: 
    def test_basic(self): 
        assert centered_moving_average([1, 2, 3, 4, 5], 3) == [2.0, 3.0, 4.0] 
  
    def test_even_window_raises(self): 
        with pytest.raises(ValueError, match="нечётным"): 
            centered_moving_average([1, 2, 3, 4], 2) 
  
  
class TestExponentialMovingAverage: 
    def test_alpha_1_returns_original(self): 
        data = [1.0, 5.0, -2.0, 3.0] 
        assert exponential_moving_average(data, alpha=1.0) == data 
  
    def test_recursive_formula(self): 
        data = [1.0, 2.0, 3.0] 
        ema = exponential_moving_average(data, alpha=0.5) 
        assert ema == pytest.approx([1.0, 1.5, 2.25]) 
  
    @pytest.mark.parametrize("bad_alpha", [0, -0.2, 1.5]) 
    def test_alpha_out_of_range(self, bad_alpha): 
        with pytest.raises(ValueError): 
            exponential_moving_average([1, 2, 3], alpha=bad_alpha) 
  
    def test_empty_raises(self): 
        with pytest.raises(ValueError): 
            exponential_moving_average([], alpha=0.5) 
  
  
class TestBenchmarkMovingAverage: 
    def test_returns_positive_timings(self): 
        data = list(range(100)) 
        res = benchmark_moving_average(data, window=5, repeats=10) 
        assert set(res) == {"list", "deque"} 
        assert res["list"] >= 0.0 
        assert res["deque"] >= 0.0 
  
    def test_invalid_window_raises(self): 
        with pytest.raises(ValueError): 
            benchmark_moving_average([1, 2], window=5, repeats=5) 