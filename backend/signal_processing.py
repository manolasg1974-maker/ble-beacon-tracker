"""Signal processing module for BLE RSSI data using Kalman filtering."""

import numpy as np
from typing import Tuple, List
import math

class KalmanFilter:
    """1D Kalman Filter for RSSI signal smoothing."""
    
    def __init__(self, process_variance: float, measurement_variance: float, 
                 initial_state: float = 0, initial_estimate_error: float = 1):
        """Initialize Kalman filter parameters.
        
        Args:
            process_variance: Q - System uncertainty
            measurement_variance: R - Measurement uncertainty
            initial_state: x - Initial state estimate
            initial_estimate_error: P - Initial estimate error
        """
        self.q = process_variance
        self.r = measurement_variance
        self.x = initial_state
        self.p = initial_estimate_error
    
    def update(self, measurement: float) -> float:
        """Perform Kalman filter update step.
        
        Args:
            measurement: New RSSI measurement (dBm)
            
        Returns:
            Filtered state estimate
        """
        # Prediction step
        self.p = self.p + self.q
        
        # Update step
        k = self.p / (self.p + self.r)  # Kalman gain
        self.x = self.x + k * (measurement - self.x)
        self.p = (1 - k) * self.p
        
        return self.x

class RSSIProcessor:
    """Process RSSI measurements for distance estimation."""
    
    def __init__(self, reference_power: float = -59, path_loss_exponent: float = 2.0):
        """Initialize RSSI processor.
        
        Args:
            reference_power: RSSI at 1 meter (dBm)
            path_loss_exponent: Propagation loss exponent
        """
        self.reference_power = reference_power
        self.path_loss_exponent = path_loss_exponent
    
    def estimate_distance(self, rssi: float) -> float:
        """Estimate distance from RSSI value using path loss model.
        
        Args:
            rssi: RSSI measurement in dBm
            
        Returns:
            Estimated distance in meters
        """
        if rssi == 0:
            return 0
        
        ratio = rssi / self.reference_power
        if ratio < 1:
            return math.pow(10, (abs(rssi) - abs(self.reference_power)) / 
                          (10 * self.path_loss_exponent))
        return 0
    
    def smooth_rssi(self, rssi_values: List[float], window_size: int = 5) -> float:
        """Apply moving average filter to RSSI values.
        
        Args:
            rssi_values: List of RSSI measurements
            window_size: Size of moving average window
            
        Returns:
            Smoothed RSSI value
        """
        if not rssi_values:
            return 0
        
        window_size = min(window_size, len(rssi_values))
        return np.mean(rssi_values[-window_size:])

class LocationEstimator:
    """Estimate beacon location from multiple RSSI measurements."""
    
    @staticmethod
    def triangulate(distances: List[Tuple[float, float, float]]) -> Tuple[float, float]:
        """Simple trilateration from distances and beacon positions.
        
        Args:
            distances: List of (x, y, distance) tuples
            
        Returns:
            (x, y) estimated location
        """
        if len(distances) < 3:
            return (0, 0)
        
        x_sum, y_sum = 0, 0
        weight_sum = 0
        
        for x, y, dist in distances:
            if dist > 0:
                weight = 1 / (dist ** 2 + 0.1)  # Inverse distance weighting
                x_sum += x * weight
                y_sum += y * weight
                weight_sum += weight
        
        if weight_sum > 0:
            return (x_sum / weight_sum, y_sum / weight_sum)
        return (0, 0)
