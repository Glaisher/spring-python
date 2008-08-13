"""
   Copyright 2006-2008 SpringSource (http://springsource.com), All Rights Reserved

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.       
"""
import unittest
from springpython.context import XmlApplicationContext
from springpython.security import AuthenticationServiceException
from springpython.security.providers.encoding import PasswordEncoder
from springpython.security.userdetails import User

class SaltedUser(User):
    def __init__(self, username, password, enabled):
        super(SaltedUser, self).__init__(username, password, enabled)
    def getUserId(self):
        return self.username

class EncodingInterfacesTestCase(unittest.TestCase):
    def testPasswordEncoderInterface(self):
        passwordEncoder = PasswordEncoder()
        self.assertRaises(NotImplementedError, passwordEncoder.encodePassword, None, None)
        self.assertRaises(NotImplementedError, passwordEncoder.isPasswordValid, None, None, None)
                
class ReflectionSaltSourceErrorTestCase(unittest.TestCase):
    def setUp(self):
        self.appContext = XmlApplicationContext("support/encodingApplicationContext.xml")
        self.user = SaltedUser("user1", "testPassword", True)

    def testEncodingWithReflectionSaltSourceNoSuchMethod(self):
        saltSource = self.appContext.getComponent("reflectionSaltSource2")
        self.assertRaises(AuthenticationServiceException, saltSource.getSalt, self.user)
        
    def testEncodingWithReflectionSaltSourceLeftEmpty(self):
        saltSource = self.appContext.getComponent("reflectionSaltSource3")
        self.assertRaises(AuthenticationServiceException, saltSource.getSalt, self.user)
        
class PlaintextPasswordEncodingTestCase(unittest.TestCase):
    
    def setUp(self):
        self.appContext = XmlApplicationContext("support/encodingApplicationContext.xml")
        self.user = SaltedUser("user1", "testPassword", True)
        self.encoder = self.appContext.getComponent("plainEncoder")
        
    def testEncodingWithNoPasswordAndNoSaltSource(self):
        encodedPassword = self.encoder.encodePassword(None, None)
        self.assertTrue(self.encoder.isPasswordValid(encodedPassword, "", None))
        
    def testEncodingWithMixedCaseAndNoSaltSource(self):
        self.encoder.ignorePasswordCase = True
        encodedPassword = self.encoder.encodePassword("TESTPASSWORD", None)
        self.assertTrue(self.encoder.isPasswordValid(encodedPassword, "testpassword", None))
        self.encoder.ignorePasswordCase = False
        
    def testEncodingWithNoSaltSource(self):
        encodedPassword = self.encoder.encodePassword(self.user.password, None)
        self.assertTrue(self.encoder.isPasswordValid(encodedPassword, self.user.password, None))
        
    def testEncodingWithSystemWideSaltSourceLeftEmpty(self):
        saltSource = self.appContext.getComponent("systemWideSaltSource")
        salt = saltSource.getSalt(self.user)
        encodedPassword = self.encoder.encodePassword(self.user.password, salt)
        self.assertTrue(self.encoder.isPasswordValid(encodedPassword, self.user.password, salt))
        
    def testEncodingWithSystemWideSaltSourceConfigured(self):
        saltSource = self.appContext.getComponent("systemWideSaltSource2")
        salt = saltSource.getSalt(self.user)
        encodedPassword = self.encoder.encodePassword(self.user.password, salt)
        self.assertTrue(self.encoder.isPasswordValid(encodedPassword, self.user.password, salt))
        
    def testEncodingWithSystemWideSaltSourceInvalidLeftBrace(self):
        saltSource = self.appContext.getComponent("systemWideSaltSource3")
        salt = saltSource.getSalt(self.user)
        self.assertRaises(ValueError, self.encoder.encodePassword, self.user.password, salt)
        
    def testEncodingWithSystemWideSaltSourceInvalidRightBrace(self):
        saltSource = self.appContext.getComponent("systemWideSaltSource4")
        salt = saltSource.getSalt(self.user)
        self.assertRaises(ValueError, self.encoder.encodePassword, self.user.password, salt)
        
    def testEncodingWithSystemWideSaltSourceInvalidBothBraces(self):
        saltSource = self.appContext.getComponent("systemWideSaltSource5")
        salt = saltSource.getSalt(self.user)
        self.assertRaises(ValueError, self.encoder.encodePassword, self.user.password, salt)
        
    def testEncodingWithReflectionSaltSourceConfigured(self):
        saltSource = self.appContext.getComponent("reflectionSaltSource")
        salt = saltSource.getSalt(self.user)
        encodedPassword = self.encoder.encodePassword(self.user.password, salt)
        self.assertTrue(self.encoder.isPasswordValid(encodedPassword, self.user.password, salt))
        
class Md5PasswordEncodingTestCase(unittest.TestCase):
    
    def setUp(self):
        self.appContext = XmlApplicationContext("support/encodingApplicationContext.xml")
        self.user = SaltedUser("user1", "testPassword", True)
        self.encoder = self.appContext.getComponent("md5Encoder")

    def testEncodingWithNoPasswordAndNoSaltSource(self):
        encodedPassword = self.encoder.encodePassword(None, None)
        self.assertTrue(self.encoder.isPasswordValid(encodedPassword, "", None))
        
    def testEncodingWithMixedCaseAndNoSaltSource(self):
        self.encoder.ignorePasswordCase = True
        encodedPassword = self.encoder.encodePassword("TESTPASSWORD", None)
        self.assertTrue(self.encoder.isPasswordValid(encodedPassword, "testpassword", None))
        self.encoder.ignorePasswordCase = False
        
    def testEncodingWithNoSaltSource(self):
        encodedPassword = self.encoder.encodePassword(self.user.password, None)
        self.assertTrue(self.encoder.isPasswordValid(encodedPassword, self.user.password, None))
        
    def testEncodingWithSystemWideSaltSourceLeftEmpty(self):
        saltSource = self.appContext.getComponent("systemWideSaltSource")
        salt = saltSource.getSalt(self.user)
        encodedPassword = self.encoder.encodePassword(self.user.password, salt)
        self.assertTrue(self.encoder.isPasswordValid(encodedPassword, self.user.password, salt))
        
    def testEncodingWithSystemWideSaltSourceConfigured(self):
        saltSource = self.appContext.getComponent("systemWideSaltSource2")
        salt = saltSource.getSalt(self.user)
        encodedPassword = self.encoder.encodePassword(self.user.password, salt)
        self.assertTrue(self.encoder.isPasswordValid(encodedPassword, self.user.password, salt))
        
    def testEncodingWithSystemWideSaltSourceInvalidLeftBrace(self):
        saltSource = self.appContext.getComponent("systemWideSaltSource3")
        salt = saltSource.getSalt(self.user)
        encodedPassword = self.encoder.encodePassword(self.user.password, salt)
        self.assertTrue(self.encoder.isPasswordValid(encodedPassword, self.user.password, salt))
        
    def testEncodingWithSystemWideSaltSourceInvalidRightBrace(self):
        saltSource = self.appContext.getComponent("systemWideSaltSource4")
        salt = saltSource.getSalt(self.user)
        encodedPassword = self.encoder.encodePassword(self.user.password, salt)
        self.assertTrue(self.encoder.isPasswordValid(encodedPassword, self.user.password, salt))
        
    def testEncodingWithSystemWideSaltSourceInvalidBothBraces(self):
        saltSource = self.appContext.getComponent("systemWideSaltSource5")
        salt = saltSource.getSalt(self.user)
        encodedPassword = self.encoder.encodePassword(self.user.password, salt)
        self.assertTrue(self.encoder.isPasswordValid(encodedPassword, self.user.password, salt))
        
    def testEncodingWithReflectionSaltSourceConfigured(self):
        saltSource = self.appContext.getComponent("reflectionSaltSource")
        salt = saltSource.getSalt(self.user)
        encodedPassword = self.encoder.encodePassword(self.user.password, salt)
        self.assertTrue(self.encoder.isPasswordValid(encodedPassword, self.user.password, salt))

class ShaPasswordEncodingTestCase(unittest.TestCase):
    
    def setUp(self):
        self.appContext = XmlApplicationContext("support/encodingApplicationContext.xml")
        self.user = SaltedUser("user1", "testPassword", True)
        self.encoder = self.appContext.getComponent("shaEncoder")

    def testEncodingWithNoPasswordAndNoSaltSource(self):
        encodedPassword = self.encoder.encodePassword(None, None)
        self.assertTrue(self.encoder.isPasswordValid(encodedPassword, "", None))
        
    def testEncodingWithMixedCaseAndNoSaltSource(self):
        self.encoder.ignorePasswordCase = True
        encodedPassword = self.encoder.encodePassword("TESTPASSWORD", None)
        self.assertTrue(self.encoder.isPasswordValid(encodedPassword, "testpassword", None))
        self.encoder.ignorePasswordCase = False
        
    def testEncodingWithNoSaltSource(self):
        encodedPassword = self.encoder.encodePassword(self.user.password, None)
        self.assertTrue(self.encoder.isPasswordValid(encodedPassword, self.user.password, None))
        
    def testEncodingWithSystemWideSaltSourceLeftEmpty(self):
        saltSource = self.appContext.getComponent("systemWideSaltSource")
        salt = saltSource.getSalt(self.user)
        encodedPassword = self.encoder.encodePassword(self.user.password, salt)
        self.assertTrue(self.encoder.isPasswordValid(encodedPassword, self.user.password, salt))
        
    def testEncodingWithSystemWideSaltSourceConfigured(self):
        saltSource = self.appContext.getComponent("systemWideSaltSource2")
        salt = saltSource.getSalt(self.user)
        encodedPassword = self.encoder.encodePassword(self.user.password, salt)
        self.assertTrue(self.encoder.isPasswordValid(encodedPassword, self.user.password, salt))
        
    def testEncodingWithSystemWideSaltSourceInvalidLeftBrace(self):
        saltSource = self.appContext.getComponent("systemWideSaltSource3")
        salt = saltSource.getSalt(self.user)
        encodedPassword = self.encoder.encodePassword(self.user.password, salt)
        self.assertTrue(self.encoder.isPasswordValid(encodedPassword, self.user.password, salt))
        
    def testEncodingWithSystemWideSaltSourceInvalidRightBrace(self):
        saltSource = self.appContext.getComponent("systemWideSaltSource4")
        salt = saltSource.getSalt(self.user)
        encodedPassword = self.encoder.encodePassword(self.user.password, salt)
        self.assertTrue(self.encoder.isPasswordValid(encodedPassword, self.user.password, salt))
        
    def testEncodingWithSystemWideSaltSourceInvalidBothBraces(self):
        saltSource = self.appContext.getComponent("systemWideSaltSource5")
        salt = saltSource.getSalt(self.user)
        encodedPassword = self.encoder.encodePassword(self.user.password, salt)
        self.assertTrue(self.encoder.isPasswordValid(encodedPassword, self.user.password, salt))
        
    def testEncodingWithReflectionSaltSourceConfigured(self):
        saltSource = self.appContext.getComponent("reflectionSaltSource")
        salt = saltSource.getSalt(self.user)
        encodedPassword = self.encoder.encodePassword(self.user.password, salt)
        self.assertTrue(self.encoder.isPasswordValid(encodedPassword, self.user.password, salt))
        