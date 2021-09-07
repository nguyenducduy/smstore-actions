from gql import gql

query = gql("""
    mutation insertUser(
        $object: users_insert_input!
    ) {
        insert_users_one(
            object: $object
        ) {
            id
        }
    }
""")