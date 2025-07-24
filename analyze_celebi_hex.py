#!/usr/bin/env python3

# Analyze the Celebi hex dump to find correct byte positions
# Based on known values: Species=251 (Celebi), Level should be reasonable, etc.

hex_data = """
00000000: ed2c 2d2e 0000 e891 fb00 0000 c9d3 0000  .,-.............
00000010: 142c 1000 1e00 0100 0000 0000 3db6 3f97  .,..........=.?.
00000020: 0f0f 0900 0000 0000 0000 0000 0000 0000  ................
00000030: 0000 0000 0000 0000 0000 0000 0000 0000  ................
00000040: 0000 0000 0000 0000 0000 0000 0000 0000  ................
00000050: 0000 0000 0000 0000 4300 6500 6c00 6500  ........C.e.l.e.
00000060: 6200 6900 0000 0000 0000 0000 0000 0000  b.i.............
00000070: 0000 4c01 6900 b101 5e00 140a 050a 0000  ..L.i...^.......
00000080: 0000 0000 0000 0000 0000 5501 ffff ff29  ..........U....)
00000090: 0000 0000 0000 0000 0000 0000 0000 0000  ................
000000a0: 0000 0000 0000 0000 b203 b103 b503 b203  ................
000000b0: b103 b503 0000 0000 0000 0000 0000 0000  ................
000000c0: 0000 0102 0100 0000 6401 0405 2c00 0000  ........d...,...
000000d0: 0000 0000 0000 0000 0000 0000 0000 2800  ..............(.
000000e0: 0000 0200 0000 0000 ff00 0000 0000 0000  ................
000000f0: 0000 0000 0000 0000 7400 7300 7500 6e00  ........t.s.u.n.
00000100: 0000 0000 0000 0000 0000 0000 0000 0000  ................
00000110: 0000 6400 0000 0000 0000 0000 110c 1100  ..d.............
00000120: 0000 4175 041e 0000 0000 0000 0000 0000  ..Au............
00000130: 0000 0000 0092 bff6 65df f4c4 3d00 0000  ........e...=...
00000140: 0000 0000 0000 0000 6400 5501 d400 ec00  ........d.U.....
00000150: ec00 0301 e100 0000                      ........
"""

print("Analyzing Celebi PK8 hex dump...")

# Convert hex data to bytes
data_bytes = []
for line in hex_data.strip().split('\n'):
    hex_part = line.split(':')[1].split('  ')[0].strip()
    hex_bytes = hex_part.replace(' ', '')
    for i in range(0, len(hex_bytes), 2):
        if i + 1 < len(hex_bytes):
            data_bytes.append(int(hex_bytes[i:i+2], 16))

print(f"Total bytes: {len(data_bytes)}")

# Known values to look for:
# - Species: 251 (0xFB) - should be at bytes 8-9 as little endian
# - Nickname: "Celebi" in UTF-16 - should be around 0x58

print("\nAnalyzing key positions:")

# Check species at different positions
for pos in [8, 10, 12, 14]:
    if pos + 1 < len(data_bytes):
        species = data_bytes[pos] + (data_bytes[pos + 1] << 8)
        print(f"Position {pos:02X}: {species} (0x{species:04X})")

print(f"\nBytes 8-9: {data_bytes[8]:02X} {data_bytes[9]:02X} = {data_bytes[8] + (data_bytes[9] << 8)} (species)")

# Look for reasonable level values (1-100)
print(f"\nLooking for level (1-100):")
for pos in range(0x70, 0x90):
    if pos < len(data_bytes) and 1 <= data_bytes[pos] <= 100:
        print(f"Position 0x{pos:02X} ({pos}): {data_bytes[pos]} - possible level")

# Look for nature (0-24)
print(f"\nLooking for nature (0-24):")
for pos in range(0x20, 0x50):
    if pos < len(data_bytes) and 0 <= data_bytes[pos] <= 24:
        print(f"Position 0x{pos:02X} ({pos}): {data_bytes[pos]} - possible nature")

# Look for friendship (typically 70-255)
print(f"\nLooking for friendship:")
for pos in range(0xA0, 0xE0):
    if pos < len(data_bytes) and 50 <= data_bytes[pos] <= 255:
        print(f"Position 0x{pos:02X} ({pos}): {data_bytes[pos]} - possible friendship")

# Check specific interesting positions
print(f"\nSpecific position analysis:")
print(f"0x1E (30): {data_bytes[0x1E]} - potential level")
print(f"0x20 (32): {data_bytes[0x20]} - potential nature") 
print(f"0x74 (116): {data_bytes[0x74]} - potential level")
print(f"0x8C (140): {data_bytes[0x8C]}")
print(f"0xCA (202): {data_bytes[0xCA]} - potential friendship")

# Look for IV patterns (should be 0-31 each)
print(f"\nLooking for IV patterns:")
print(f"Around 0x7C: {data_bytes[0x7C]:02X} {data_bytes[0x7D]:02X} {data_bytes[0x7E]:02X} {data_bytes[0x7F]:02X}")

# Check if there are 32-bit packed IVs
for pos in range(0x70, 0x90, 4):
    if pos + 3 < len(data_bytes):
        iv_value = (data_bytes[pos] + 
                   (data_bytes[pos+1] << 8) + 
                   (data_bytes[pos+2] << 16) + 
                   (data_bytes[pos+3] << 24))
        
        # Extract individual IVs from 32-bit value
        iv_hp = iv_value & 31
        iv_attack = (iv_value >> 5) & 31  
        iv_defense = (iv_value >> 10) & 31
        iv_speed = (iv_value >> 15) & 31
        iv_sp_attack = (iv_value >> 20) & 31
        iv_sp_defense = (iv_value >> 25) & 31
        
        print(f"Position 0x{pos:02X}: IV32=0x{iv_value:08X}")
        print(f"  HP:{iv_hp} ATK:{iv_attack} DEF:{iv_defense} SPE:{iv_speed} SPA:{iv_sp_attack} SPD:{iv_sp_defense}")
        
        # Check if all IVs are reasonable (0-31)
        if all(0 <= iv <= 31 for iv in [iv_hp, iv_attack, iv_defense, iv_speed, iv_sp_attack, iv_sp_defense]):
            print(f"  ^ This looks like valid IVs!")