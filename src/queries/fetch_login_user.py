from gql import gql

query = gql("""
    query fetchLoginUser(
        $where: users_bool_exp
    ) {
        users(
            where: $where
        ) {
            id
            full_name
            password
            store {
                id
            }
        }
    }
""")