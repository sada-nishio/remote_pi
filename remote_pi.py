#!/usr/bin/env python
# -*- coding: utf_8 -*-

from kintone_sdk4python import Kintone
import subprocess
import sys

def main():
    #kintoneの認証情報
    domain = 'hw1xj.cybozu.com'
    token = 'oBYHrhxrC3l5FyL8wMlJK2ilNzLahiJp8pLG1Ser'
    app = 329
    query = 'flag in ("まだ！！")'

    #kinotoneに新規レコードが存在するかチェック
    try:
        kintone = Kintone()
        kintone.set_domain(domain)
        kintone.set_token_auth(token)
        response = kintone.get_records(app, query)
        records = response['records']
    except:
        print('Error: kintone.get_records is failed.')
        return 1
    #存在した場合、赤外線LEDでONを送信
    if (len(records) > 0):
        #lircを実行
        try:
            cmd = 'irsend SEND_ONCE aircon on'
            output = subprocess.check_output(cmd.strip().split(' '))
            print('Info: irsend Success!')
        except:
            print(output)
            print('Error: irsend Failed!')
            return 1

        #レコードのフラグを実行済みに更新
        record_num = records[0]['レコード番号']['value']
        try:
            record = {
                'flag': {
                    'value': '実行済！！'
                }
            }
            put_resp = kintone.put_record(app, record_num, record)
            print(put_resp)
        except:
            print('Error: kintone.put_record is failed.')
            return 1

        print('Info: success!!.')
        #正常終了
        return 0
    else:
        print('Info: no records.')
        return 0

if __name__ == '__main__':
    sys.exit(main())