# Mantiene la PC despierta mientras corre la fila de la noche, y la lanza.
Add-Type -Namespace Win32 -Name Power -MemberDefinition '[DllImport("kernel32.dll")] public static extern uint SetThreadExecutionState(uint esFlags);'
[Win32.Power]::SetThreadExecutionState(0x80000001) | Out-Null   # ES_CONTINUOUS | ES_SYSTEM_REQUIRED: no suspender
try {
    & "C:\Program Files\Git\bin\bash.exe" "/c/Users/eoinb/projects/labo2/scripts/cola_noche.sh"
} finally {
    [Win32.Power]::SetThreadExecutionState(0x80000000) | Out-Null   # vuelve a lo normal
}
