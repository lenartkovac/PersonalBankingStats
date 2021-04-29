import numpy as np

nkbm = {
    #? subscriptions
    "destiny": 4.45,
    "netflix": 11.95,
    "telekom": 75.62,
    "iCloud": 2.99,
    "lastFM": 3.00,
    "wanikani": 7.51,
    "spotify": 11.99,
    "a1": 29.99,

    #? food
    "limbo": 14.50,
    "ostrozno": 19.26,
    "interspar": 84.86,
    "wolt": 42.9,

    #? other
    "loccitane": 27.90,
    "riot": 20.0,
    "cleverBridge": 19.95,
    "lastpass": 31.84
}


bills = np.sum([nkbm.get(key) for key in ["telekom", "a1"]])
subscriptions = np.sum([nkbm.get(key) for key in ["destiny", "netflix", "iCloud", "lastFM", "wanikani", "spotify"]])
food = np.sum([nkbm.get(key) for key in ["interspar", "ostrozno", "limbo", "wolt"]])
other = np.sum([nkbm.get(key) for key in ["loccitane", "riot", "cleverBridge", "lastpass"]])
total = np.sum(list(nkbm.values()))

print(f"bills:         \t{bills}€")
print(f"subscriptions: \t{subscriptions}€")
print(f"food:          \t{food}€")
print(f"other:         \t{other}€")
print(f"total:         \t{total}€ == {bills + subscriptions + food + other}€")