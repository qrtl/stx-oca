Due to a technical limitation, we cannot use http.db_list() to respect dbfilter
during module loading, as HTTP configuration is not available at that stage.
Therefore, db.list_dbs() is used instead. As a result, blacklist domains from inactive databases
will also affect running databases.
