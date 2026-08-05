from geometry import Bearing, fault_frequencies

fImpact = 3000
decay = 1000
duration_seconds = 1.0

cwru_bearing = Bearing("CWRU 6205",
               9,
               7.94,
               39.04,
               contact_angle=0.0)

freqs = fault_frequencies(cwru_bearing, 1.0)
