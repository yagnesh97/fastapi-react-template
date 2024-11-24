#!/bin/bash
set -e

# Hash the password using Python
USER_PASSWORD_HASH=$(python3 -c "
import bcrypt, base64
password = '$MONGO_INITDB_ROOT_PASSWORD'
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
# Convert hashed password to base64 to avoid issues with special characters
binary_hash = base64.b64encode(hashed).decode()
print(binary_hash)")

# Get the current timestamp in ISO 8601 format
CURRENT_DATE=$(date --utc +"%Y-%m-%dT%H:%M:%S.%3NZ")

# Use the hashed password when adding the record to the users collection
mongosh <<EOF
use admin
db.createUser({
  user: '$MONGO_INITDB_ROOT_USERNAME',
  pwd:  '$MONGO_INITDB_ROOT_PASSWORD',
  roles: [{
    role: 'readWrite',
    db: '$MONGO_INITDB_DATABASE'
  }]
})

use $MONGO_INITDB_DATABASE
db.users.insertOne({
  username: '$MONGO_INITDB_ROOT_USERNAME',
  hashed_password: BinData(0, '$USER_PASSWORD_HASH'),
  email: '$MONGO_INITDB_ROOT_EMAIL',
  first_name: 'admin',
  last_name: 'admin',
  admin: true,
  active: true,
  created_by: '$MONGO_INITDB_ROOT_USERNAME',
  created_date: ISODate("$CURRENT_DATE"),
  updated_by: '$MONGO_INITDB_ROOT_USERNAME',
  updated_date: ISODate("$CURRENT_DATE")
})
EOF
