# grpcurl Quick Setup (Windows)

## Method 1: winget (Fastest)

Open PowerShell/Terminal:

```powershell
winget install --id fullstorydev.grpcurl --exact
```

Open a **new** terminal, then verify:

```powershell
grpcurl --version
```

---

## Method 2: Scoop (Fallback)

Open a **normal, non-admin** PowerShell window:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
irm get.scoop.sh | iex
```

Close and reopen PowerShell, then install:

```powershell
scoop install grpcurl
grpcurl --version
```

---

## Quick Test

From the repo's `protos` folder (it contains `challenge.proto`):

```powershell
cd protos
'{"problem_id": 1}' | grpcurl -plaintext -import-path . -proto challenge.proto -d '@' 54.37.231.25:50051 challenge.TopologyService/DescribeStructure
```

You should get a JSON reply containing `"problemId": 1`.

> Note: `grpcurl` is a standalone gRPC CLI, not the regular `curl` command.
>
> In PowerShell, pipe the JSON in (`'...' | grpcurl ... -d '@'`) as shown. Passing it
> inline with `-d '{...}'` breaks in Windows PowerShell 5.1, which strips the quotes.
>
> `grpcurl -plaintext 54.37.231.25:50051 list` fails with *"server does not support the
> reflection API"*. That is expected: always pass `-import-path . -proto challenge.proto`.
