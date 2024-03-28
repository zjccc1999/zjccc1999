@echo off
chcp 65001
setlocal

set "DOMAIN=txt.zjccc.xyz"
set "TOKEN=zjccc"

rem %~nx1表示第一个参数的文件名和扩展名
set "FILENAME=%~nx1"

rem PowerShell命令读取文件的前65行内容，将内容转换为UTF8并进行base64编码
for /f "delims=" %%i in ('powershell -command "$content = ((Get-Content -Path '%cd%/%FILENAME%' -Encoding Default) | Select-Object -First 65) -join [Environment]::NewLine; [convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes($content))"') do set "BASE64_TEXT=%%i"

rem 将内容保存到response.txt
rem echo %BASE64_TEXT% > response.txt

rem 构造带有文件名和内容作为参数的URL
set "URL=https://%DOMAIN%/%FILENAME%?token=%TOKEN%^&b64=%BASE64_TEXT%"

rem 显示请求的响应 
rem powershell -Command "(Invoke-WebRequest -Uri '%URL%').Content"
start %URL%
endlocal

echo 更新数据完成,倒数5秒后自动关闭窗口...
timeout /t 5 >nul
exit