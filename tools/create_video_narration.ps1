param(
    [Parameter(Mandatory = $true)][string]$StoryboardPath,
    [Parameter(Mandatory = $true)][string]$OutputDirectory
)

$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Speech

New-Item -ItemType Directory -Force -Path $OutputDirectory | Out-Null
$storyboard = Get-Content -LiteralPath $StoryboardPath -Raw -Encoding UTF8 | ConvertFrom-Json
$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
$synth.SelectVoice('Microsoft Sabina Desktop')
$synth.Rate = 0
$synth.Volume = 100

try {
    for ($index = 0; $index -lt $storyboard.Count; $index++) {
        $fileName = 'voice-{0:D2}.wav' -f ($index + 1)
        $outputPath = Join-Path $OutputDirectory $fileName
        $synth.SetOutputToWaveFile($outputPath)
        $synth.Speak([string]$storyboard[$index].voiceover)
        $synth.SetOutputToNull()
        Write-Output $outputPath
    }
}
finally {
    $synth.Dispose()
}
