---
layout: llm_change
title: "Linting for buggy copy.py"
date: 2025-04-03T13:54:18.840404
file: "evaluate/buggy copy.py"
change_type: "Linting"
consolidated: true
---
--- original
+++ fixed
@@ -28,4 +28,4 @@
 def list_index_error():
     """Return a valid element from the list to avoid IndexError."""
     local_list = [1, 2, 3]
-    return local_list[0]
+    return local_list[0]