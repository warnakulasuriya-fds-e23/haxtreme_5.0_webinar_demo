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

Replace `localhost:5001` with your server address:

```powershell
grpcurl -plaintext localhost:5001 list
```

> Note: `grpcurl` is a standalone gRPC CLI, not the regular `curl` command.
