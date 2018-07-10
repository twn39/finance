import os
import sys
import json
import yaml
import logging
from flask import Flask
from flask import request
from waitress import serve
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client


logging.basicConfig(level=logging.INFO, stream=sys.stdout)
app = Flask(__name__)


@app.route('/data', methods=['POST'])
def fetch_data():
    code = request.form['code']
    start = request.form['from']
    end = request.form['to']
    config_yaml = yaml.load(open('config.yaml', encoding="utf-8"))
    config_cdn = config_yaml['CDN']
    command = u'Rscript ./finance.R -c "{0}" -f "{1}" -t "{2}"'.format(code, start, end)
    status = os.system(command)
    file_name = '{0}{1}{2}.png'.format(code, start, end)

    if status == 0:

        secret_id = config_cdn['secret_id']  # 替换为用户的 secretId
        secret_key = config_cdn['secret_key']  # 替换为用户的 secretKey
        region = config_cdn['region']  # 替换为用户的 Region
        token = ''  # 使用临时密钥需要传入 Token，默认为空，可不填
        config = CosConfig(Secret_id=secret_id, Secret_key=secret_key, Region=region, Token=token)
        # 2. 获取客户端对象
        client = CosS3Client(config)
        path = './images/{0}'.format(file_name)

        with open(path, 'rb') as fp:
            client.put_object(
                Bucket=config_cdn['bucket'],
                Body=fp,
                Key=file_name,
                StorageClass='STANDARD',
                ContentType='text/html; charset=utf-8'
            )

    return json.dumps({
        'url': 'https://{0}.cos.{1}.myqcloud.com/{2}'.format(config_cdn['bucket'], config_cdn['region'], file_name)
    })


if __name__ == '__main__':
    serve(app, listen='*:5000')
