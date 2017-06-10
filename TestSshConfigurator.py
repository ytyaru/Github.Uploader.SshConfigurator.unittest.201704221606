import unittest
from SshConfigurator import SshConfigurator
class TestSshConfigurator(unittest.TestCase):
    def test_Load_NonePath(self):
        c = SshConfigurator()
        c.Load()
        self.assertTrue(True)
    def test_Load(self):
        c = SshConfigurator()
        c.Load(path='test_config')
        self.assertEqual(2, len(c.Hosts))
    def test_Host_Names(self):
        c = SshConfigurator()
        c.Load(path='test_config')
        self.assertIn('github.com.user0', c.Hosts.keys())
        self.assertIn('github.com.user1', c.Hosts.keys())
    def test_Host0_Keys(self):
        c = SshConfigurator()
        c.Load(path='test_config')
        self.assertIn('Host', c.Hosts['github.com.user0'])
        self.assertIn('HostName', c.Hosts['github.com.user0'])
        self.assertIn('User', c.Hosts['github.com.user0'])
        self.assertIn('IdentityFile', c.Hosts['github.com.user0'])
        self.assertIn('TCPKeepAlive', c.Hosts['github.com.user0'])
        self.assertIn('IdentitiesOnly', c.Hosts['github.com.user0'])
    def test_Host0_Values(self):
        c = SshConfigurator()
        c.Load(path='test_config')
        self.assertIn('github.com.user0', c.Hosts['github.com.user0']['Host'])
        self.assertIn('github.com', c.Hosts['github.com.user0']['HostName'])
        self.assertIn('git', c.Hosts['github.com.user0']['User'])
        self.assertIn('22', c.Hosts['github.com.user0']['Port'])
        self.assertIn('~/.ssh/rsa_4096_user0', c.Hosts['github.com.user0']['IdentityFile'])
        self.assertIn('yes', c.Hosts['github.com.user0']['TCPKeepAlive'])
        self.assertIn('yes', c.Hosts['github.com.user0']['IdentitiesOnly'])
    def test_AppendAndDelete(self):
        # Hostを追加し削除する
        # * 他のテストに影響を与えないようにするため追加したら削除する
        # * 何度やっても同じ結果になるようにするため追加したら削除する
        username = 'user55'
        host = 'github.com.' + username
        IdentityFile = '~/.ssh/rsa_4096_' + username
        Port = '55'
        # 初回は存在しない
        c = SshConfigurator()
        c.Load(path='test_config')
        self.assertEqual(2, len(c.Hosts))
        self.assertTrue(not(host in c.Hosts.keys()))
        # 追加したら存在する
        c.AppendHost(username, IdentityFile, Port=Port)
        c.Load(path='test_config')
        self.assertEqual(3, len(c.Hosts))
        self.assertIn(host, c.Hosts.keys())
        self.assertEqual(host, c.Hosts[host]['Host'])
        self.assertEqual(IdentityFile, c.Hosts[host]['IdentityFile'])
        self.assertEqual(Port, c.Hosts[host]['Port'])
        # 削除したら消える
        c.DeleteHost(host)
        c.Load(path='test_config')
        self.assertEqual(2, len(c.Hosts))
        self.assertTrue(not(host in c.Hosts.keys()))
    """
    複数Host書き込んでも正常に読み取れるか。
    改行が足りなくて前後の定義とつながるなどの不具合が生じないか。
    """
    def test_MultiAppend(self):
        c = SshConfigurator()
        c.Load(path='test_config')
        # Host追加
        username = 'user2'
        IdentityFile = '~/.ssh/rsa_4096_' + username
        c.AppendHost(username, IdentityFile)
        username = 'user3'
        IdentityFile = '~/.ssh/rsa_4096_' + username
        c.AppendHost(username, IdentityFile)
        c.Load(path='test_config') # 意味なく間でLoadする
        username = 'user4'
        IdentityFile = '~/.ssh/rsa_4096_' + username
        c.AppendHost(username, IdentityFile)    
        username = 'user5'
        IdentityFile = '~/.ssh/rsa_4096_' + username
        c.AppendHost(username, IdentityFile)
        # 確認
        c.Load(path='test_config')
        self.assertIn('github.com.user0', c.Hosts.keys())
        self.assertIn('github.com.user1', c.Hosts.keys())
        self.assertIn('github.com.user2', c.Hosts.keys())
        self.assertIn('github.com.user3', c.Hosts.keys())
        self.assertIn('github.com.user4', c.Hosts.keys())
        self.assertIn('github.com.user5', c.Hosts.keys())
        # 後始末
        c.DeleteHost('github.com.user2')
        c.DeleteHost('github.com.user3')
        c.DeleteHost('github.com.user4')
        c.DeleteHost('github.com.user5')
    def test_GetKeyFilePath(self):
        c = SshConfigurator()
        c.Load(path='test_config')
        # IdentityFileに秘密鍵を指定した場合
        self.assertIn('~/.ssh/rsa_4096_user0', c.Hosts['github.com.user0']['IdentityFile'])
        self.assertEqual('~/.ssh/rsa_4096_user0', c.GetPrivateKeyFilePath('github.com.user0'))
        self.assertEqual('~/.ssh/rsa_4096_user0.pub', c.GetPublicKeyFilePath('github.com.user0'))
        # IdentityFileに公開鍵を指定した場合
        self.assertIn('~/.ssh/rsa_4096_user1.pub', c.Hosts['github.com.user1']['IdentityFile'])
        self.assertEqual('~/.ssh/rsa_4096_user1', c.GetPrivateKeyFilePath('github.com.user1'))
        self.assertEqual('~/.ssh/rsa_4096_user1.pub', c.GetPublicKeyFilePath('github.com.user1'))
