struct Prim(object)
    PEEL_OPERATIONS = {"object" => categorical_peel,
    "bool" => categorical_peel,
    "int8" => discrete_peel,
    "int16" => discrete_peel,
    "int32" => discrete_peel,
    "int64" => discrete_peel,
    "uint8" => discrete_peel,
    "uint16" => discrete_peel,
    "uint32" => discrete_peel,
    "uint64" => discrete_peel,
    "float16" => real_peel,
    "float32" => real_peel,
    "float64" => real_peel}

PASTE_OPERATIONS = {"object" => categorical_paste,
     "bool" => categorical_paste,
     "int8" => discrete_peel,
     "int16" => real_paste,
     "int32" => real_paste,
     "int64" => real_paste,
     "uint8" => discrete_peel,
     "uint16" => real_paste,
     "uint32" => real_paste,
     "uint64" => real_paste,
     "float16" => real_paste,
     "float32" => real_paste,
     "float64" => real_paste}
     
     #dictionaries to determine which method to use 
     #dependent on the dtype