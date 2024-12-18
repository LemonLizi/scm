"""import org.apache.commons.codec.digest.DigestUtils;
//导入md5加密需要用的库
import org.apache.commons.codec.binary.Base64;
import java.io.ByteArrayOutputStream;
import java.security.Key;
import java.security.KeyFactory;
import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.security.PrivateKey;
import java.security.PublicKey;
import java.security.Signature;
import java.security.interfaces.RSAPrivateKey;
import java.security.interfaces.RSAPublicKey;
import java.security.spec.PKCS8EncodedKeySpec;
import java.security.spec.X509EncodedKeySpec;
import java.util.HashMap;
import java.util.Map;
import javax.crypto.Cipher;
import java.net.URLEncoder;
导入rsa方法需要用的库

log.info("foo 123 ---------");
//测试引用库是否全部成
String RSA_PUB_KEY = "${rsaPublicKey}";
//公钥
String KEY_ALGORITHM = "RSA";
String SIGNATURE_ALGORITHM = "MD5withRSA";
int MAX_ENCRYPT_BLOCK = 117;
int MAX_DECRYPT_BLOCK = 128;

public static byte[] encryptByPublicKey(byte[] data, String publicKey) throws Exception {
    byte[] keyBytes = Base64.decodeBase64(publicKey);
    X509EncodedKeySpec x509KeySpec = new X509EncodedKeySpec(keyBytes);
    KeyFactory keyFactory = KeyFactory.getInstance(KEY_ALGORITHM);
    Key publicK = keyFactory.generatePublic(x509KeySpec);
    // 对数据加密
    Cipher cipher = Cipher.getInstance(keyFactory.getAlgorithm());
    cipher.init(Cipher.ENCRYPT_MODE, publicK);
    int inputLen = data.length;
    ByteArrayOutputStream out = new ByteArrayOutputStream();
    int offSet = 0;
    byte[] cache;
    int i = 0;
    // 对数据分段加密
    while (inputLen - offSet > 0) {
        if (inputLen - offSet > MAX_ENCRYPT_BLOCK) {
            cache = cipher.doFinal(data, offSet, MAX_ENCRYPT_BLOCK);
        } else {
            cache = cipher.doFinal(data, offSet, inputLen - offSet);
        }
        out.write(cache, 0, cache.length);
        i++;
        offSet = i * MAX_ENCRYPT_BLOCK;
    }
    byte[] encryptedData = out.toByteArray();
    out.close();
    return encryptedData;
}
String md5_str="NIRUOanhao321";
//设置转换md5的密码
String md5_psw = DigestUtils.md5Hex(md5_str);
//得到转换为md5的密码
log.info(md5_psw);
//打印一下看看有没有拿到数据

vars.put("md5",md5_psw);

long time = Long.parseLong("${__time(,)}");
//把当前时间戳设置为变量
String str = md5_psw + time;
//定义需要rsa加密的字符串（我们现在是md5加密后+时间戳包起来再rsa加密）
log.info("haha123 "+str+", "+time);
log.info("haha123111 "+time);
//打印看一下格式是否正确，查看一下加密前的时间戳

String result = "";

try {
    result = Base64.encodeBase64String(encryptByPublicKey(str.getBytes(), RSA_PUB_KEY));
    log.info("foo 123123123-----");

    result1 = encryptByPublicKey(str.getBytes(), RSA_PUB_KEY);
    System.out.println(result);
} catch(Exception e) {
    // TODO Auto-generated catch block
    e.printStackTrace();
}

log.info("foo result: "+result);
//打印看一下加密得到的结果
vars.put("rsa_pwd", result);
//rsa_pwd是jmeter脚本中引用的变量名
vars.put("now_time", ""+time);
//拿到当前时间戳设置的变量
"""