# practice-cicd

## Initial Settings
1. EC2インスタンスに ssh 接続
1. root にログイン
    ```
    # sudo su -
    ```
1. pyenv を使って Python v3.10.1 をインストール
    ```
    # CONFIGURE_OPTS="--with-openssl=/usr/local/openssl-1.1.1/" pyenv install -v 3.10.1
    # pyenv global 3.10.1
    ```