#### 安装
基础依赖安装使用pip install即可，例如nltk, jieba等，根据运行提示安装缺少的依赖。

对于standford coreNLP的安装，首先下载 http://nlp.stanford.edu/software/stanford-corenlp-full-2018-10-05.zip 并解压缩，然后下载 http://nlp.stanford.edu/software/stanford-chinese-corenlp-2018-10-05-models.jar 中文扩展，并将此jar包放入解压缩的文件夹内。最后在main.py中206行的文件夹地址改为解压缩的地址即可。

#### 特殊提示：
1.审批人配置在resource/myDict.dict中，姓名可以模糊匹配。

2.请假时间三个要素：开始时间、时长、结束时间，三个必须满足两个。时长最小单位可以为半天。

3.请假理由一般为动宾短语或是整句，有时会出现bug，可以记录并反馈。

4.邮箱格式必须满足 xx@xx.xx 。

5.最后提示是否确认，若不确认将会清空。

#### 测试用例：
1. 我要请假去看病，让杨慧宇帮我批一下，从明天到周五。

2. 你好，我想请个事假，我要去开家长会。六月十八号下午请半天假。

3. 我想请个假。

   后天起请三天假。
   
   杨慧禹
