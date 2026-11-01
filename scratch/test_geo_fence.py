# -*- coding: utf-8 -*-
import math

def haversine(lat1, lon1, lat2, lon2):
    R = 6371e3
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlam = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlam/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# Test 1: Exactly same spot
d1 = haversine(13.847621, 100.569432, 13.847621, 100.569432)
print(f"Test 1 (Same spot): {d1:.1f} m -> Within 500m: {d1 <= 500}")

# Test 2: 150 meters away
d2 = haversine(13.847621, 100.569432, 13.848500, 100.570000)
print(f"Test 2 (Nearby spot): {d2:.1f} m -> Within 500m: {d2 <= 500}")

# Test 3: 4.5 km away (e.g. Laksi to KU)
d3 = haversine(13.847621, 100.569432, 13.884500, 100.578600)
print(f"Test 3 (Far spot): {d3:.1f} m -> Within 500m: {d3 <= 500}")

assert d1 <= 500
assert d2 <= 500
assert d3 > 500
print("Haversine assertions passed!")

