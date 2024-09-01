# madr-fastapi-course
Meu Acervo Digital de Romances (conclusão do curso "FastAPI do Zero" do @dunossauro)

### Running the project

With docker, run the following command:

```
docker-compose up
```

This will create and start the containers.

The following URLs will be available:

```
Application:
http://localhost:8000/

PgAdmin:
http://localhost:5050/
```

If the PostgreSQL complains about permissions, you can run this command in the `data/` persistency folder in project root:

```
sudo chmod -R 777 data
```

### To Do

- Finish the tests
