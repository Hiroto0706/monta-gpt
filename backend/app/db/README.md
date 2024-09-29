# 新しいmigration fileの作成方法

```
alembic revision -m $(name)

# 例
alembic revision -m "create_user_table"
```

# migration up

```
# 最新のバージョンまでmigrationを実行
alembic upgrade head

# count分だけmigrationを実行
alembic upgrade +${count}
```

# migration down

```
# すべてのmigrationをdownさせる
alembic downgrade base

# count分だけmigrationをdown
alembic downgrade -${count}
```
