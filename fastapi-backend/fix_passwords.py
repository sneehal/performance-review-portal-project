# fix_passwords.py
try:
	# preferred import
	from passlib.hash import bcrypt
except Exception:
	# fallback for environments where the package layout differs or static
	# analysis cannot resolve the import
	from passlib.handlers.bcrypt import bcrypt

password = "Test@1234"
hashed   = bcrypt.hash(password)

print("Hash  :", hashed)
print("Valid :", bcrypt.verify(password, hashed))
print()
print("-- Run this SQL in Oracle:")
print(f"UPDATE USERS SET password_hash = '{hashed}' WHERE 1=1;")
print("COMMIT;")