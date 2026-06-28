param(
    [Parameter(Mandatory = $true)]
    [string]$Registry,
    [ValidateSet('latest', 'dev')]
    [string]$Tag = 'dev'
)

$ErrorActionPreference = 'Stop'
$Image = "$Registry/tempconverter:$Tag"

docker build --build-arg "IMAGE_VARIANT=$Tag" --tag $Image .
docker push $Image
Write-Host "Published $Image"
