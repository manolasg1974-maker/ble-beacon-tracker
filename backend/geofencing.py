"""Geofencing module for BLE beacon zone management."""

from typing import List, Tuple, Optional
from enum import Enum
import math
from datetime import datetime

class EventType(Enum):
    """Types of geofence events."""
    ENTER = "enter"
    EXIT = "exit"
    DWELL = "dwell"
    MOVEMENT = "movement"

class Geofence:
    """Circular geofence zone."""
    
    def __init__(self, zone_id: str, center_x: float, center_y: float,
                 radius: float, name: str = ""):
        """Initialize geofence.
        
        Args:
            zone_id: Unique identifier
            center_x: X coordinate of center
            center_y: Y coordinate of center
            radius: Radius in meters
            name: Friendly name
        """
        self.zone_id = zone_id
        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius
        self.name = name
    
    def contains_point(self, x: float, y: float) -> bool:
        """Check if point is within geofence.
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            True if point is inside geofence
        """
        distance = math.sqrt((x - self.center_x)**2 + (y - self.center_y)**2)
        return distance <= self.radius
    
    def distance_to_point(self, x: float, y: float) -> float:
        """Calculate distance from point to geofence center.
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            Distance in meters
        """
        return math.sqrt((x - self.center_x)**2 + (y - self.center_y)**2)

class GeofenceManager:
    """Manage multiple geofences and track beacon events."""
    
    def __init__(self):
        """Initialize geofence manager."""
        self.geofences: List[Geofence] = []
        self.beacon_states: dict = {}  # beacon_id -> set of zone_ids
    
    def add_geofence(self, geofence: Geofence) -> None:
        """Add geofence to manager.
        
        Args:
            geofence: Geofence object
        """
        self.geofences.append(geofence)
    
    def check_events(self, beacon_id: str, x: float, y: float) -> List[Tuple[str, EventType]]:
        """Check for geofence events based on beacon location.
        
        Args:
            beacon_id: Beacon identifier
            x: X coordinate
            y: Y coordinate
            
        Returns:
            List of (zone_id, event_type) tuples
        """
        events = []
        current_zones = set()
        
        # Check which zones contain the beacon
        for geofence in self.geofences:
            if geofence.contains_point(x, y):
                current_zones.add(geofence.zone_id)
        
        # Get previous zones
        previous_zones = self.beacon_states.get(beacon_id, set())
        
        # Detect ENTER events (new zones)
        for zone_id in current_zones - previous_zones:
            events.append((zone_id, EventType.ENTER))
        
        # Detect EXIT events (left zones)
        for zone_id in previous_zones - current_zones:
            events.append((zone_id, EventType.EXIT))
        
        # Update state
        self.beacon_states[beacon_id] = current_zones
        
        return events

class GeofenceEvent:
    """Record a geofence event."""
    
    def __init__(self, beacon_id: str, zone_id: str, event_type: EventType,
                 timestamp: Optional[datetime] = None):
        """Initialize geofence event.
        
        Args:
            beacon_id: Beacon identifier
            zone_id: Zone identifier
            event_type: Type of event
            timestamp: Event timestamp
        """
        self.beacon_id = beacon_id
        self.zone_id = zone_id
        self.event_type = event_type
        self.timestamp = timestamp or datetime.utcnow()
    
    def to_dict(self) -> dict:
        """Convert event to dictionary.
        
        Returns:
            Dictionary representation
        """
        return {
            'beacon_id': self.beacon_id,
            'zone_id': self.zone_id,
            'event_type': self.event_type.value,
            'timestamp': self.timestamp.isoformat()
        }
