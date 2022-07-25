# Ironsight API v2

FastAPI backend for managing hypervisor virtual machines, containers, users, networks, etc.

## ⚠️ Warning ⚠️

**This is NOT a finished project, it is highly experimental and unreliable! Do NOT use this in a production environment!**

## Currently supported hypervisors

![Proxmox](https://camo.githubusercontent.com/a83e76f7cb663d3bcd9e49130941b9e11923b2bee22c1a57b17e8b75baa9e75b/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f50726f786d6f782d4535373030303f7374796c653d666f722d7468652d6261646765266c6162656c436f6c6f723d626c61636b266c6f676f3d70726f786d6f78266c6f676f436f6c6f723d7768697465)

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

## Ironsight API Migration Progress

- [ ] getVMList()
- [ ] getLabList()
- [ ] getTemplateList()
- [ ] getNewsList()
- [ ] getDocCount()
- [ ] getCPUUsage()
- [ ] getNetworkUsage()
- [ ] getMemoryUsage()
- [ ] getMetrics()
- [ ] getDiskUsage()
- [ ] getVMCPUUsage()
- [ ] getVMMemoryUsage()
- [ ] getVMNetworkPacketsReceived()
- [ ] getVMNetworkPacketsSent()
- [ ] getNumVMsOn()
- [ ] getNumVMs()
- [ ] getVMsOn()
- [ ] getLabOverview()
- [ ] getCourseList()
- [ ] getTags()
- [ ] getUsersList()
- [ ] getRoles()
- [ ] getPermissions()
- [ ] getHarvesterVMList()
- [ ] getActivityLog()
- [ ] getBashHistory()
- [ ] getRunningProcesses()
- [ ] getFileMonitoring()
- [ ] handleEvent() (Seek alternative)
- [ ] postActivityLog()
- [ ] powerOnVM()
- [ ] authenticate()

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
