# Ironsight API v2

FastAPI backend for managing hypervisor virtual machines, containers, users, networks, etc.

## ⚠️ Warning ⚠️

**This is NOT a finished project, it is highly experimental and unreliable! Do NOT use this in a production environment!**

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`HYPERVISOR`

`HYPERVISOR_URL` (without the trailing slash `/`)

`HYPERVISOR_TOKEN_ID`

`HYPERVISOR_SECRET_KEY`

## Deployment

To deploy this project run

```bash
uvicorn main:ironsight_api --reload
```

## API Reference

### REST API

For all REST API requests, you will need your API key

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `api_key` | `string` | **Required**. Your API key |

#### Get API information

```http
  GET /
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `api_key` | `string` | **Required**. Your API key |

#### Get API server health

```http
  GET /health
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `api_key` | `string` | **Required**. Your API key |

### Python API

Set up your hypervisor object:

```python
import hypervisors
hypervisor = hypervisors.init_hypervisor(HYPERVISOR)
```

#### Get API information

```python
  getSummary()
```

| Parameter | Type | Description |
| :-------- | :--- | :---------- |
| None      |      |             |

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Contributing

Contributions are always welcome!
