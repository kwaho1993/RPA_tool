# class Animal:
#     def __init__(self, name, age, **kwargs):
#         self.name = name
#         self.age = age
#         super().__init__(**kwargs)

# class Walker:
#     def __init__(self, walking_speed, **kwargs):
#         self.walking_speed = walking_speed
#         super().__init__(**kwargs)

# class Swimmer:
#     def __init__(self, swimming_speed, **kwargs):
#         self.swimming_speed = swimming_speed
#         super().__init__(**kwargs)

# class Dog(Animal, Walker, Swimmer):
#     def __init__(self, name, age, walking_speed, swimming_speed):
#         super().__init__(name=name, age=age, walking_speed=walking_speed, swimming_speed=swimming_speed)

# # 클래스 사용 예시
# my_dog = Dog("Buddy", 5, 3, 1.5)
# print(my_dog.get_info())      # Buddy is 5 years old.
# print(my_dog.get_abilities()) # Walking at 3 km/h and Swimming at 1.5 m/s.

import os
import pandas as pd
from datetime import datetime, timedelta
import calendar

exe_folder = os.path.dirname(os.path.abspath(__file__))

non_dynamicDB_dir = os.path.join(exe_folder, 'Database', 'non-Dynamic')
dynamicDB_dir = os.path.join(exe_folder, 'Database', 'Dynamic')


# DB 간 공통 속성을 1개 이상 포함하도록 한다.

# 정적 DB
CSV_QC_ID = fr'{non_dynamicDB_dir}\QC_ID_data.csv'

# 동적 DB
CSV_QC_RESULT = fr'{dynamicDB_dir}\QC_RESULT_data.csv'
CSV_QC_LOT = fr'{dynamicDB_dir}\QC_LOT_data.csv'
CSV_QC_TARGET = fr'{dynamicDB_dir}\QC_TARGET_data.csv'

DB = { 'QC_ID'        : pd.read_csv(CSV_QC_ID, encoding='CP949'),
       'QC_RESULT'    : pd.read_csv(CSV_QC_RESULT, encoding='CP949'),
       'QC_LOT'       : pd.read_csv(CSV_QC_LOT, encoding='CP949'),
       'QC_TARGET'    : pd.read_csv(CSV_QC_TARGET, encoding='CP949')
}

# DB 관련 메소드 모음 클래스
class DB_MANAGER:
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def get_LIST(self, DB_name:str, column_name:str):
        """
        원하는 DB에서 원하는 컬럼을 중복제거,정렬하여 리스트로 리턴
        : 검사코드('code'), 검사명('name'), 정도관리ID('ID'), 담당자('position') 등의 명단을 얻는데 활용

        예시: print(DB_MANAGER().get_LIST('QC_ID','ID'))
        """
        list_ = DB[DB_name][column_name].drop_duplicates().sort_values().tolist()
        return list_
    

# 장비
class Equipment:
    """
    param : 장비명
    """
    def __init__(self, name_Equipment, **kwargs) -> None:
        super().__init__(**kwargs)
        self.name_Equipment = name_Equipment    # 장비명
        self.manufacturer = ''  # 제조사

# 검사
class Test:
    """
    param : 검사코드
    """
    def __init__(self, code_Test:str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.code_Test = code_Test  # 검사코드
        self.name_Test = ''  # 검사명
        self.slip = ''  # 슬립
        self.isQual = ''  # 정성="Qualitative", 정량="Quantitative", 반정량="semi-Quantitative"
        self.personal = ''  # 담당자 (ex: "EIA")
        self.unit = ''  # 단위
        self.start_Test = '' # 검사 시작일
        self.end_Test = '' # 검사 종료일

# LOT
class LOT:
    """
    param : LOT번호
    """
    def __init__(self, lot:str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.lot = lot   # LOT 번호
        self.exp = ""   # EXP 날짜
        self.start_LOT = "" # LOT 시작일
        self.end_LOT = ""   # LOT 종료일
        self.inHouse = False    # 자가제조=True, 업체시약=False
        self.change_with = ""   # level별로 관리되는지, kit별로 관리되는지

    def sync_QC_LOT():
        # AMIS와 QC LOT DB 가 일치하는지 순회하면서 확인한다.
        return


# 허용범위
class AcceptableRange(Test):
    def __init__(self, code_Test:str, **kwargs) -> None:
        super().__init__(code_Test=code_Test, **kwargs)
        self.sync_AMIS = False  # AMIS에 입력되어있는지
        self.no_cv = False    # (NC등의 이유로) cv를 계산하지 않는지

        self.start_AcceptableRange = ""   # 허용범위 시작일
        self.complete_AcceptableRange = ""   # 허용범위 설정 완료일
        self.end_AcceptableRange = ""   # 허용범위 사용종료일

        self.data = []  # 허용범위 설정 데이터
        self.mean_AcceptableRange = float() # 타겟 mean
        self.sd_AcceptableRange = float()   # 타겟 sd
        self.cv_AcceptableRange = float()   # 타겟 cv

        self.reset_reasons  = []    # 허용범위 재설정 사유(QC LOT변경, 시약LOT변경, Trend 조정, Calibration)


# QC
class QC:
    """
    param : 정도관리 ID
    """
    # def __init__(self) -> None:
    def __init__(self, QC_ID:str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.QC_ID = QC_ID     # 정도관리 ID
        self.name_QC = ""   # QC 이름
        self.level = ""     # 농도
        self.condition_QCpass = bool()  # QC 통과 조건

    def call_Data(self, from_date:str = None, to_date:str = None):
        """
        특정 기간 내의 정도관리 데이터를 df로 리턴
        """
        df = DB['QC_RESULT']
        df = df = df.loc[(df['ID'] == self.QC_ID)]

        # 'date'컬럼, 매개변수들을 datetime 객체로
        df['date'] = pd.to_datetime(df['date'], format='%Y%m%d', errors='coerce')
        if from_date : 
            from_ = datetime.strptime(from_date, "%Y%m%d")
            df = df.loc[(df['date'] >= from_)]

        if to_date :
            to_ = datetime.strptime(to_date, "%Y%m%d")
            df = df.loc[(df['date'] <= to_)]

        return df
    
    def call_Statics(self, from_date:str, to_date:str):
        """
        특정 기간 내의 mean, sd, cv를 리턴
        """
        # 특정 기간 내의 데이터 중 'result' 컬럼
        results = self.call_Data(from_date, to_date)['result'].astype(float)

        # 통계량 계산
        mean = float(results.mean())
        sd = float(results.std())
        cv = float(sd/mean)

        return {"mean": mean, "sd": sd, "cv": cv}
    
    def call_SDI_Data(self, from_date:str, to_date:str):
        """
        특정 기간 내의 SDI값 데이터를 리턴

        예시: print(QC('ZDA00184').call_SDI_Data(from_date="20240701", to_date="20240731"))
        """
        # df_qc와 df_target를 가져와서 yyyymmdd를 datetime으로 바꿔준다
        df_qc = self.call_Data(from_date, to_date)
        df_target = DB['QC_TARGET'].loc[DB['QC_TARGET']["ID"] == self.QC_ID]
        df_target['start_date'] = pd.to_datetime(df_target['start_date'], format='%Y%m%d', errors='coerce')

        # df_qc의 각 행의 date를 기준으로, 해당 date이하의 최대값을 df_target의 start_date에서 찾는다.
        qc_dates = df_qc['date'].tolist()
        target_dates = pd.to_datetime(df_target['start_date'], format='%Y%m%d', errors='coerce')
        target_date_matches = [max([date for date in target_dates if date < qc_date])
                               for qc_date in qc_dates]
        
        # 찾아낸 start_date들을 matched_target_date 컬럼에 추가
        df_qc['matched_target_date'] = target_date_matches

        # matched_target_date 에 해당하는 mean, sd를 가져온다.
        df_qc = df_qc.merge(df_target[['start_date', 'mean', 'sd']], left_on='matched_target_date', right_on='start_date', how='left')

        # float으로 타입변경 후 SDI 컬럼 계산
        df_qc[['result', 'mean', 'sd']] = df_qc[['result', 'mean', 'sd']].astype(float)
        df_qc['SDI'] = (df_qc['result'] - df_qc['mean']) / df_qc['sd']

        called_data = df_qc.drop(columns=['equipment', 'matched_target_date'])

        return called_data

    def call_LOT_byDate(self, yyyymmdd:str=None):
        """
        시작일을 기준으로 LOT을 리턴한다.

        예시 : print(QC('Z5115012').call_LOT_byDate('20240621'))
        """
        df = DB['QC_LOT']
        df['start_date'] = df['start_date'].astype(str)
        trimmed_df = df.loc[(df['ID'] == self.QC_ID)
                             & (df['start_date'] == yyyymmdd)].reset_index(drop=True)
        if len(trimmed_df):
            return trimmed_df.loc[0,'LOT']
        else:
            return None
    


    def recent_LOT(self, index=0, yyyymm:str=None):
        """
        최근 index 번째(0부터 시작)의 LOT과 lot 시작일을 dict로 반환

        예시 : print(QC('ZDA00184').recent_LOT(index=2))
        """
        df = DB['QC_LOT']   # QC_LOT 데이터베이스 호출

        # yyyymm이 입력되면, 해당월의 마지막날짜 이전의 데이터만 따진다.
        if yyyymm:
            _, last_day = calendar.monthrange(int(yyyymm[:4]), int(yyyymm[-2:]))
            df = DB['QC_LOT'].loc[DB['QC_LOT']['start_date'] <= int(f'{yyyymm}{last_day}')]

        df = df.loc[df['ID'] == self.QC_ID].sort_values('start_date', ascending=False)  # 정도관리ID 기준으로 LOT 정리
        df = df[['start_date', 'LOT']].reset_index(drop=True)

        result = {'start_date' : str(df.loc[index, 'start_date']),
               'LOT' : df.loc[index, 'LOT']}

        return result
    
    def recent_TARGET_reset(self, index=0, yyyymm:str = None):
        """
        최근 index 번째(0부터 시작)의 target data를 반환

        예시 : print(QC('ZDA00184').recent_TARGET_reset())
        """
        df = DB['QC_TARGET']   # QC_TARGET 데이터베이스 호출

        # yyyymm이 입력되면, 해당월의 마지막날짜 이전의 데이터만 따진다.
        if yyyymm:
            _, last_day = calendar.monthrange(int(yyyymm[:4]), int(yyyymm[-2:]))
            df = DB['QC_TARGET'].loc[DB['QC_TARGET']['start_date'] <= int(f'{yyyymm}{last_day}')]

        df = df.loc[df['ID'] == self.QC_ID].sort_values('start_date', ascending=False).reset_index(drop=True).iloc[index]  # 정도관리ID 필터, 인덱스리셋

        return df
    
    def lot_cummulate_df(self, lot:str=None, index=0, yyyymm:str = None):
        """
        LOT 누적 QC result df 리턴

        yyyymm -> 해당 월의 마지막 날짜 기준, 그 이전만 따짐
        lot -> 해당 LOT의 lot 누적(index 매개변수무시됨)
        """

        # DB['QC_LOT']
        recent_LOT_infoDict = self.recent_LOT(index=index)

        # recent_LOT_change = self.recent_LOT(index=index)['start_date']

        if yyyymm:
            recent_LOT_infoDict = self.recent_LOT(index=index, yyyymm=yyyymm)

        if lot:
            try:
                i = index
                while recent_LOT_infoDict['LOT'] != lot:
                    i = i+1
                    recent_LOT_infoDict = self.recent_LOT(index=i, yyyymm=yyyymm)
            except:
                print("parameter로 주어진 LOT이 최근 리스트에 없습니다.")
                raise IndexError
            
        recent_LOT_change = recent_LOT_infoDict['start_date']

        df = self.call_Data(from_date=recent_LOT_change)

        return df
    

    def monthly_statics(self, yyyymm):

        _, last_day = calendar.monthrange(int(yyyymm[:4]), int(yyyymm[-2:]))
        df_yyyymm = self.call_Data(f'{yyyymm}01', f'{yyyymm}{last_day}')

        # 1. 기준 LOT 구하기 & 해당월 유효 df 구하기
        used_LOT = self.recent_LOT(index=0, yyyymm=yyyymm) # 기본적으로 최근 LOT을 선택
        used_current_Month_df = df_yyyymm   # 기본적으로 1일~마지막일 df를 선택

        # 1-1. yyyymm 내에 LOT변경이 있었다면, 다수 결과가 있는 LOT 선택
        # 1-1-1. 예외 조건 설정        
        recent_lot_change = used_LOT['start_date'] # 최근 LOT 변경일자
        dt_recent_lot_change= datetime.strptime(recent_lot_change, '%Y%m%d')    # 최근 LOT 변경일자(dt로 바꿈)

        is_LOT_changed = bool(len(df_yyyymm.loc[df_yyyymm['date'] == dt_recent_lot_change]))

        # 1-1-2. 예외 조건별 used_LOT 설정

        if is_LOT_changed:
            # yyyymmdd 내 다수 LOT 변경을 체크
            change_dates = [dt_recent_lot_change]
            count = 1
            try:
                while datetime.strptime(str(self.recent_LOT(index=count, yyyymm=yyyymm)['start_date']), '%Y%m%d'
                                        ) in df_yyyymm['date'].tolist():
                    change_dates.append(datetime.strptime(str(self.recent_LOT(index=count, yyyymm=yyyymm)['start_date']), '%Y%m%d'))
                    count += 1
            except:
                pass
            print(f'{yyyymm} : LOT변경 {count}회')

            # pd.cut을 사용하여 count +1 개의 구간으로 나누기
            boundaries = sorted([df_yyyymm['date'].min()] + change_dates + [df_yyyymm['date'].max()])

            df_yyyymm['date_bin'] = pd.cut(df_yyyymm['date'], bins=boundaries, right=False)
            
            df_list = [df_yyyymm[df_yyyymm['date_bin'] == interval] for interval in df_yyyymm['date_bin'].cat.categories]

            try:
                # 가장 길이가 긴 df의 시작일과 같은 df를 찾아서 used_LOT으로 설정
                used_LOT = [self.recent_LOT(index=i, yyyymm=yyyymm) for i in range(count) if max(df_list, key=len)['date'].min() == datetime.strptime(str(self.recent_LOT(index=i, yyyymm=yyyymm)['start_date']), '%Y%m%d')][0]
            except:
                # 가장 길이가 긴 df의 시작일이 yyyymm01 보다 과거일 경우, index=count를 used_LOT으로 설정
                used_LOT = self.recent_LOT(index=count, yyyymm=yyyymm)
            
            # 가장 길이가 긴 df를 used_current_Month_df로 설정
            used_current_Month_df = max(df_list, key=len)

        # 1-2. 현재월 유효 df로 data 만들기
        current_mean = used_current_Month_df['result'].astype(float).mean()
        current_sd = used_current_Month_df['result'].astype(float).std()
        current_cv = current_sd / current_mean

        used_Current = {'mean': current_mean,
                       'sd': current_sd,
                       'cv': current_cv,
                       'start_date': used_current_Month_df['date'].min().strftime('%Y%m%d'),
                       'data_count': len(used_current_Month_df)
                       }



        # 2. Target 값 구하기
        used_target_df = self.recent_TARGET_reset(index=0, yyyymm=yyyymm) # 일단 최근 허용범위로 설정  
        
        # 2-1. 가장 최근 허용범위 재설정이 yyyymm 내에서 어떤상태인지 확인

        # 2-1-1. 예외 조건 설정
        recent_complete_date = str(used_target_df['complete_date'])
        is_target_resetting = bool((recent_complete_date == "nan")
                              or (recent_complete_date > f'{yyyymm}{last_day}')) # 허용범위 재설정이 진행중인가(완료되지 않았는가)
        
        dt_recent_target_reset_start= datetime.strptime(str(used_target_df['start_date']), '%Y%m%d')    # 최근 허용범위 재설정 시작일자(dt로 바꿈)
        is_target_reset_started = bool(len(df_yyyymm.loc[df_yyyymm['date'] == dt_recent_target_reset_start]))       # yyyymm 기간 내에, 허용범위 재설정 시작했는가

        # 2-1-2. 예외 조건별 used_TARGET 설정
        if is_target_resetting:
            used_target_df = self.recent_TARGET_reset(index=1, yyyymm=yyyymm)

        used_TARGET = {'mean': used_target_df['mean'],
                       'sd': used_target_df['sd'],
                       'cv': used_target_df['cv'],
                       'start_date': str(used_target_df['start_date']),
                       }
        
        # 3. LOT 누적 df 구하기
        used_LOT_cummul_df = self.lot_cummulate_df(lot=used_LOT['LOT'], yyyymm=yyyymm)

        lot_cummul_mean = used_LOT_cummul_df['result'].astype(float).mean()
        lot_cummul_sd = used_LOT_cummul_df['result'].astype(float).std()
        lot_cummul_cv = lot_cummul_sd / lot_cummul_mean

        used_LOT_cummul = {'mean': lot_cummul_mean,
                       'sd': lot_cummul_sd,
                       'cv': lot_cummul_cv,
                       'start_date': used_LOT_cummul_df['date'].min().strftime('%Y%m%d'),
                       'data_count' : len(used_LOT_cummul_df)
                       }
        
        # 4. no cv 확인하기
        df_lot = DB['QC_LOT']
        info_nocv = df_lot.loc[(df_lot['ID'] == self.QC_ID) & (df_lot['LOT'] == used_LOT['LOT']), 'info_nocv'].values[0]
        print(f'cv 정보: {str(info_nocv)}')

        # 4. 최종 데이터
        result = {'QC_ID' : self.QC_ID,
                  'LOT' : used_LOT['LOT'],
                  'start_date' : used_LOT['start_date'],

                  'target_mean' : used_TARGET['mean'],
                  'target_sd' : used_TARGET['sd'],

                  'current_mean' : used_Current['mean'],
                  'current_sd' : used_Current['sd'],
                  'current_count' : used_Current['data_count'],

                  'lot_cummul_mean' : used_LOT_cummul['mean'],
                  'lot_cummul_sd' : used_LOT_cummul['sd'],
                  'lot_cummul_count' : used_LOT_cummul['data_count'],

                  'comment' : ""
                  }
        
        if str(info_nocv) != 'nan':
            result['target_cv'] = "*"
            result['current_cv'] = "*"
            result['lot_cummul_cv'] = "*"
        else:
            result['target_cv'] = used_TARGET['cv']
            result['current_cv'] = used_Current['cv']
            result['lot_cummul_cv'] = used_LOT_cummul['cv']

        if is_target_resetting:
            original_lot_start = self.recent_TARGET_reset(index=1, yyyymm=yyyymm).tolist()[1]
            new_lot_start = self.recent_TARGET_reset(index=0, yyyymm=yyyymm).tolist()[1]

            original_lot = self.call_LOT_byDate(str(original_lot_start))
            new_lot = self.call_LOT_byDate(str(new_lot_start))

            df_yyyymm.loc[df_yyyymm['date']]

            result['comment'] = f'허용범위 설정 중: {original_lot}->{new_lot} ()'
            print(df_yyyymm)

        # comment 부분 채워넣어야함(LOT 변경시.. lot 다수변경은 어떻게?)
        
        return result


print(QC('Z5115012').monthly_statics('202406'))


# 시약
class Reagent:
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.name_Reagent = ""  # 시약명