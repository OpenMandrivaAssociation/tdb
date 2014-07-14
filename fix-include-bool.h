From: Adam Williamson <awilliam@redhat.com>
Date: Fri, 23 May 2014 10:08:14 -0700
Subject: [PATCH] tdb/include: include stdbool.h in tdb.h

Commit db5bda56bf08 (tdb: add TDB_MUTEX_LOCKING support) adds a bool, but does
not include stdbool.h. This causes any build including tdb.h to fail, at least
for me with GCC 4.9.0.
---
 lib/tdb/include/tdb.h | 1 +
 1 file changed, 1 insertion(+)

diff --git a/include/tdb.h b/include/tdb.h
index 5ea5e60..03e429c 100644
--- a/include/tdb.h
+++ b/include/tdb.h
@@ -31,6 +31,7 @@ extern "C" {
 #endif
 
 #include <signal.h>
+#include <stdbool.h>
 
 /**
  * @defgroup tdb The tdb API
-- 
1.9.3

iff -Nru tdb-1.3.0/debian/patches/series tdb-1.3.0/debian/patches/series
-- tdb-1.3.0/debian/patches/series	2014-06-02 00:41:17.000000000 +0100
++ tdb-1.3.0/debian/patches/series	2014-06-04 16:28:51.000000000 +0100
@ -1,2 +1,3 @@
missing-stdbool-include.patch
30_tdb_logging_func.diff
40_test_transaction_expand_non_fatal.diff
