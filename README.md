# 程式實作

此題目原先要求以 Python 實作，但我另外實作了 C# 版本供參考。
- Python 版本的實作放在此 repo 的 `Python` 資料夾下，程式進入點為 `main.py`
- C# 版本的實作放在此 repo 的 `CSharp` 資料夾下，Solution 為 `TestModuleSimulator.sln`，程式進入點為 `TestModuleSimulator/Program.cs`


## Python 版本的實作內容

1. 新增另外兩個模擬測試模組
	* 設計決定：新增 package `test_module`，放置下列 class
		* `AutoTestModule`，模擬自動測試 (包含原本的 auto test module 以及新增的 auto test module extra 行為)。
		* `ManualTestModule`，模擬手動測試 (manual test module 行為)。
2. 收到三個測試模組的測試結果
	* 題目有一個較為模糊的字句：「**當次的測試結果**」，有以下兩種理解：
		* 最近一次的結果：每個模組最近一次發送的結果。
		* 定期同步的結果：即使這些結果不是同時發送的，但如果在這個定期檢查時三個模組的結果都是 Pass 或都是 Fail，那麼這些結果將被記錄下來。
	* 我假設這裡的「當次」是指「最近」，也就是說，我們只需要記錄三個模組「最近」發送的結果。
	* 設計決定：新增 package `checker`，放置下列 class
		* `RecentResultChecker`，透過比對 3 個測試模組「最後」產生的測試結果來決定是否要輸出結果到 Excel 檔。
3. 輸出結果到Excel檔紀錄時間與結果，此Excel需要有前面所有的測試紀錄結果。
	* 設計決定：新增 package `writer`，放置下列 class
		* `ExcelWriter`，負責將測試結果寫入 Excel 檔，採用 append 方式以便保留原本的檔案內容，達到「需要有前面所有的測試紀錄結果」的要求。

## C# 版本的實作內容
在 C# 版本的實作中，程式架構和流程與 Python 版本類似，但是採用了 C# 語言特有的功能和語法來進行開發。

1. 新增另外兩個模擬測試模組
	* 與 Python 版本類似，新增 namespace `TestModules`，放置下列 class
		* `AutoTestModule`，模擬自動測試 (包含原本的 auto test module 以及新增的 auto test module extra 行為)。
		* `ManualTestModule`，模擬手動測試 (manual test module 行為)。

2. 收到三個測試模組的測試結果
	* 與 Python 版本類似，新增 namespace `Checker`，放置下列 class
		* `RecentResultChecker`，透過比對 3 個測試模組「最後」產生的測試結果來決定是否要輸出結果到 Excel 檔。

3. 輸出結果到Excel檔紀錄時間與結果，此Excel需要有前面所有的測試紀錄結果。
	* 與 Python 版本類似，新增 namespace `Writers`，放置下列 class
		* `ExcelWriter`，負責將測試結果寫入 Excel 檔，採用 append 方式以便保留原本的檔案內容，達到「需要有前面所有的測試紀錄結果」的要求。

## 資料流向

TestModule 執行測試 -> 判定 result (Pass or Fail) -> 傳遞 result 給 checker 進行儲存 -> checker 根據儲存的 result 決定是否要呼叫 ExcelWriter 進行結果輸出。

```
+-------------------+      +-------------------+      +-------------------+
|  AutoTestModule   |      | AutoTestModule    |      | ManualTestModule  |
|  (Every 0.5 sec)  |      | Extra (Every 1.8  |      | (3-10 sec random  |
|                   |      | sec)              |      | intervals)        |
+-------------------+      +-------------------+      +-------------------+
         |                            |                           |
         v                            v                           v
      +---------------------------------------------------------------+
      |                                                               |
      |                        receive_result                         |
      |                    (Receives test results)                    |
      |                      (Callback funtion)                       |
	  |                                                               |
      +---------------------------------------------------------------+
                                     |
                                     v
                  +-------------------------------------+
                  |                                     |
                  |               Checker               |
                  | (Stores and processes test results) |
                  |                                     |
                  +-------------------------------------+
                                     |
                                     v
                           +-------------------+
                           |                   |
                           | Excel Writer      |
                           | (Writes to Excel) |
                           |                   |
                           +-------------------+
```


## 本次題目

底下為一個模擬自動測試模組Test Module，每0.5秒會隨機傳送一個Pass或是Fail的值給統整函式receive_result並輸出文字結果並顯示時間

```python
import time
import random
import threading
import datetime as dt
from typing import AnyStr

def auto_test_module() -> AnyStr:
	while True:
		time.sleep(0.5)
		receive_result( "Pass" if random.randint(0, 1) else "Fail" )

def receive_result(test_result: AnyStr) -> None:
	print(f"{dt.datetime.now()} --> Received Result: {test_result}")

threading.Thread(target=auto_test_module, daemon=True).start()
```

現在考慮導入多工的情況，需要協助製作以下功能：

1. 請新增另外兩個模擬測試模組，並將測試結果送給receive_result：
	A. auto test module extra - 每1.8秒發送一次隨機結果(Pass or Fail)
	B. manual test module - 每次發送測試結果後隨機挑選3-10秒來設定為下次發送前的時間間隔，此項為模擬人手動測試的情況

2. 請重新設計函式receive result，並完成以下目標：
	A. 可以收到三個測試模組的測試結果
	B. 當三個測試模組當次的測試結果同時為Pass或Fail時輸出結果到Excel檔紀錄時間與結果，此Excel需要有前面所有的測試紀錄結果。

Note. 範例程式為最簡化的方式設計，在修改程式時請請盡量以優化的方式來進行，一些未陳述詳盡的地方可自行定義，並以註解的形式加註在程式碼內。