import wmi

c = wmi.WMI()
l = []
for process in c.Win32_Process():
    l += [int(process.ProcessId), process.Name]

l = sorted(l)

for i in l:
    print(i)
