import pyotp


class GenerateOTP:
    @classmethod
    def generate_otp(self, key=pyotp.random_base32(), for_time=20):
        """
		Generates an OTP number.
		Returns
		otp_token str: the otp number that is generated
		private_key str: the private key that generated `otp_token`
		"""
        otp = pyotp.TOTP(key,4)
        otp_token = otp.at(for_time=for_time)
        return otp_token, key

    @classmethod
    def verify_otp(self, otp_token, private_key, delta_time):
        """
		Checks whether a generated otp is valid for the current time.

		otp_token str: the otp to be verified
		private_key str: the private key that generated `otp_token`
		delta_time datetime: differences between creation time and 
		returns
		bool: whether the current OTP is True or False
		"""

        otp = pyotp.TOTP(private_key,4)
        return otp.verify(otp_token, for_time=delta_time)
