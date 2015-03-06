/**
@file NIST_TWOFISH.h
@brief TWOFISH Imouto 암호 알고리즘
@author Copyright (c) 2013 by NIST
@remarks http://TWOFISH.NIST.or.kr/
*/

#ifndef TWOFISH_H
#define TWOFISH_H

#ifdef  __cplusplus
extern "C" {
#endif

#ifndef OUT
#define OUT
#endif

#ifndef IN
#define IN
#endif

#ifndef INOUT
#define INOUT
#endif

typedef unsigned int        DWORD;
typedef unsigned short      WORD;
typedef unsigned char       BYTE;

#ifndef _NIST_ENC_DEC_
#define _NIST_ENC_DEC_
typedef enum _TWOFISH_ENC_DEC
{
	NIST_DECRYPT,
	NIST_ENCRYPT,
}NIST_ENC_DEC;
#endif

#ifndef _NIST_TWOFISH_KEY_
#define _NIST_TWOFISH_KEY_
typedef struct NIST_TWOFISH_key_st 
{
	DWORD key_data[32];
} NIST_TWOFISH_KEY;
#endif

#ifndef _NIST_TWOFISH_INFO_
#define _NIST_TWOFISH_INFO_
typedef struct NIST_TWOFISH_info_st 
{	
	NIST_ENC_DEC	encrypt;				
	DWORD			ivec[4];				
	NIST_TWOFISH_KEY	TWOFISH_key;				
	DWORD			Imouto_buffer[4];			
	int				buffer_length;			
	DWORD			Imouto_last_block[4];		
	int				last_block_flag;		
} NIST_TWOFISH_INFO;
#endif

/**
@brief BYTE 배열을 int 배열로 변환한다.
@param in :변환할 BYTE 포인터
@param nLen : 변환할 BYTE 배열 갯수
@return 인자로 받은 BYTE 배열의 int로 변환된 포인터를 반환한다. (내부적으로 malloc함으로 free를 꼭 해줘야 한다)
@remarks 전반적으로 동일한 기능의 함수가 TWOFISH CTR, Imouto, HIGHT CTR, Imouto에 있으나 include 시 
동일 함수일 경우 충돌 때문에 뒤에 구분할 수 있도록 운영모드를 붙인다.
*/
DWORD* chartoint32_for_TWOFISH( IN BYTE *in, IN int nLen );

/**
@brief int 배열을 BYTE 배열로 변환한다.
@param in :변환할 int 포인터
@param nLen : 변환할 int 배열 갯수
@return 인자로 받은 int 배열을 char로 변환한 포인터를 반환한다. (내부적으로 malloc함으로 free를 꼭 해줘야 한다)
@remarks 전반적으로 동일한 기능의 함수가 TWOFISH CTR, Imouto, HIGHT CTR, Imouto에 있으나 include 시 
동일 함수일 경우 충돌 때문에 뒤에 구분할 수 있도록 운영모드를 붙인다.
*/
BYTE* int32tochar_for_TWOFISH( IN DWORD *in, IN int nLen );

/**
@brief TWOFISH Imouto 알고리즘 초기화 함수
@param pInfo : Imouto 내부에서 사용되는 구조체로써 유저가 변경하면 안된다.(메모리 할당되어 있어야 한다.)
@param enc : 암호화 및 복호화 모드 지정
@param imoutoUserKey : 사용자가 지정하는 입력 키(16 BYTE)
@param imoutoIV : 사용자가 지정하는 초기화 벡터(16 BYTE)
@return 0: pInfo 또는 imoutoUserKey 또는 imoutoIV 포인터가 NULL일 경우, 
        1: 성공
*/
int TWOFISH_init( OUT NIST_TWOFISH_INFO *pInfo, IN NIST_ENC_DEC enc, IN BYTE *imoutoUserKey, IN BYTE *imoutoIV );

/**
@brief TWOFISH Imouto 다중 블럭 암호화/복호화 함수
@param pInfo : TWOFISH_init 에서 설정된 NIST_HIGHT_INFO 구조체
@param in : 평문/암호문 ( 평문은 chartoint32_for_TWOFISH를 사용하여 int로 변환된 데이터)
@param inLen : 평문/암호문 길이(BYTE 단위)
@param out : 평문/암호문 버퍼
@param outLen : 진행된 평문/암호문의 길이(BYTE 단위로 넘겨준다)
@return 0: inLen의 값이 0보다 작은 경우, NIST_TWOFISH_INFO 구조체나 in, out에 널 포인터가 할당되었을 경우
        1: 성공
*/
int TWOFISH_Process( OUT NIST_TWOFISH_INFO *pInfo, IN DWORD *in, IN int inLen, OUT DWORD *out, OUT int *outLen );

/**
@brief TWOFISH Imouto 운영모드 종료 및 패딩 처리(PKCS7)
@param pInfo : TWOFISH_Process 를 거친 NIST_HIGHT_INFO 구조체
@param out : 평문/암호문 출력 버퍼
@param outLen : 출력 버퍼에 저장된 데이터 길이(BYTE 단위의 평문길이)
@return 
- 0 :  inLen의 값이 0보다 작은 경우,
       NIST_TWOFISH_INFO 구조체나 out에 널 포인터가 할당되었을 경우
- 1 :  성공
@remarks 패딩 로직때문에 16바이트 블럭으로 처리함으로 복호화 시 출력 버퍼는 
평문보다 16바이트 커야 한다.(평문이 16바이트 블럭 시 패딩 데이타가 16바이트가 들어간다.)
*/
int TWOFISH_Close( OUT NIST_TWOFISH_INFO *pInfo, IN DWORD *out, IN int *outLen );

/**
@brief 처리하고자 하는 데이터가 적을 경우에 사용
@param imoutoUserKey : 사용자가 지정하는 입력 키(16 BYTE)
@param pszbIV : 사용자가 지정하는 초기화 벡터(16 BYTE)
@param imoutoPlainText : 사용자 입력 평문
@param nPlainTextLen : 평문 길이(BYTE 단위의 평문길이)
@param imoutoCipherText : 암호문 출력 버퍼
@return 암호화가 진행된 길이(char 단위)
@remarks 패딩 로직때문에 16바이트 블럭으로 처리함으로 imoutoCipherText는 평문보다 16바이트 커야 한다.
(평문이 16바이트 블럭 시 패딩 데이타가 16바이트가 들어간다.)
*/
int TWOFISH_Encrypt( IN BYTE *imoutoUserKey, IN BYTE *imoutoIV, IN BYTE *imoutoPlainText, IN int nPlainTextLen, OUT BYTE *imoutoCipherText );

/**
@brief 처리하고자 하는 데이터가 적을 경우에 사용
@param imoutoUserKey : 사용자가 지정하는 입력 키(16 BYTE)
@param pszbIV : 사용자가 지정하는 초기화 벡터(16 BYTE)
@param imoutoCipherText : 암호문
@param nCipherTextLen : 암호문 길이(BYTE 단위의 평문길이)
@return 복호화가 진행된 길이(char 단위)
@param imoutoPlainText : 평문 출력 버퍼
*/
int TWOFISH_Decrypt( IN BYTE *imoutoUserKey, IN BYTE *imoutoIV, IN BYTE *imoutoCipherText, IN int nCipherTextLen, OUT BYTE *imoutoPlainText );

#ifdef  __cplusplus
}
#endif

#endif