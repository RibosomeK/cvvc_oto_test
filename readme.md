
A small script to check cvvc oto smoothness or accuracy.

## Independent
A presamp.ini file as a dict file.
Python version 3.8 or above is needed but the script was test on 3.10.
autoCVVC plugin or other parser plugin is needed.
Basic python knowledge.

## Usage
Open oto_test.py file and modify main() function in line 86.
add lines as follow
```python
def main():
    test = OTO_Test()
    # to read presamp.ini
    test.read_presamp('presamp.ini file path') 
    # to test vc that contain specific consonant
    test.test_consonant(['c1', 'c2', ...], 'pitch like C4')
    # save vc test ust
    test.save_ust('the path of the ust, default is result.ust')
    # to test all vv or specific ones
    test.test_vv('pitch like C4', ['v1', 'v2', ...])
    # don't forget to save vv ust
    test.save_ust('the path of ust, be sure it is different from vc ust if there is one')
```

In short, if you have a presamp file in the same folder of the script and want to test vc smoothness of z, zh, c, ch, j, q and all vv components in the pitch of A3, the main() function is as followed. 
```python
def main():
    test = OTO_Test()
    test.read_presamp('presampCHN.ini')
    test.test_consonant(('z', 'zh', 'j', 'q', 'c', 'ch'), 'A3')
    test.save_ust('vc_test.ust')
    test.test_vv('A3')
    test.save_ust('vv_test.ust')
```


# CVVC oto 测试脚本
该脚本用来检测 cvvc oto 的连续性或准确性，如某些 vc 部的滑顺程度或者 vv 部红线有没有对上拍子

# 准备
需要一个 presamp.ini 文件作为字典
理论上最低需要的 Python 版本为 3.8，但是测试版本为 3.10
生成的 ust 工程需要 autoCVVC 等类似插件进行拆音，本脚本不提供相关拆音服务
懂的基本的 Python 语法

# 用法
打开 oto_test.py 并依据自己的需要修改位于 86 行开始的 main() 函数
```python
def main():
    test = OTO_Test()
    # 读取 presamp.ini
    test.read_presamp('presamp.ini 的路径') 
    # 测试包含某些辅音的 vc 部
    test.test_consonant(['辅音1', '辅音2', ...], '音高，例如 C4')
    # 保存测试的 ust
    test.save_ust('ust 文件的路径，默认为 result.ust')
    # 测试所有的 vv 部（留空）或者某些元音的 vv 部
    test.test_vv('音高，例如 C4', ['元音1', '元音2', ..., 如果测试所有的则留空只需要填音高])
    # 不要忘记保存测试的ust
    test.save_ust('ust 工程的路径，当心不要和上面的 vc 部测试工程路径重合，否则会被覆盖。')
```

如果你想要测试刚窝好的 A3 窝头，看看辅音（z, zh, c, ch, j, q）的 vc 部的连贯性以及所有 vv 部的红线有没有放对，那 main() 函数的代码如下： 
```python
def main():
    test = OTO_Test()
    test.read_presamp('presampCHN.ini')
    test.test_consonant(('z', 'zh', 'j', 'q', 'c', 'ch'), 'A3')
    test.save_ust('vc_test.ust')
    test.test_vv('A3')
    test.save_ust('vv_test.ust')
```
保存的工程会在脚本的文件夹里，分别为 vc_test.ust 和 vv_test.ust。
其中 vc_test.ust 里音符的格式为（以辅音 z 为例）：

>R, a, za, R, ai, za, R ...

即 za 和每个元音 v 组成 [v][za][R] 的重复
另外 vv_test.ust 里音符的格式为（以元音 a 为例）：

>R, a, a, R, R, a, a, R, R, ai, a, R, R, ai, a, R, R ...

即 a 和每个元音 v 组成 [v][a][R][R] [v][a][R][R] 的重复，推荐导出后丢到 daw 中带节拍器去听拍子。