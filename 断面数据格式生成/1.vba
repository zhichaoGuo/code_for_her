Option Explicit

Sub mike11_02()

    Columns("D:H").Select
    Selection.ClearContents
    If (Range("J2").Text = "") Then
        MsgBox "请输入topid:"
       Exit Sub
     ElseIf (Range("J3").Text = "") Then
      MsgBox "请输入河流名称:"
       Exit Sub
        ElseIf (Range("J4").Text = "") Then
      MsgBox "请输入阻力系数:"
       Exit Sub
        ElseIf (Range("J5").Text = "") Then
      MsgBox "桩号前缀："
       Exit Sub

        ElseIf (Range("A1").Text = "") Then
      MsgBox "请按格式输入断面数据:"
       Exit Sub
    End If
    Dim ar
    '这个ar是表头，是断面数据的前21行内容
    ar = Array("*****************************", "TOPID", "河流名称", "里程", "COORDINATES", "0", "FLOW DIRECTION", "0", "DATUM", "0", "RADIUS TYPE", "0", "DIVIDE X-Section", "0", "SECTION ID", "  ", "INTERPOLATED", "0", "ANGLE", "0.00   0", "PROFILE  ")
    '分别存入top id 和河流名称
    ar(1) = Range("J2").Text
    ar(2) = Range("J3").Text
    Dim zulixishu As Double
    zulixishu = Range("J4").Value               '阻力系数赋值
    Dim flag1 As String
    flag1 = "SURFACE LINE:"
    Dim line_index As Long
    line_index = 1
    Dim write_line_index As Long
    write_line_index = 0
    Dim first_pile_prefix As String,prefix As String,cur_pile As String,cur_pile_m As String,cur_pile_km As String
    Dim prefix_len As Integer
    prefix_len = Len(Range("J5"))
    prefix = Range("J5")
    first_pile_prefix = Left(Cells(1, 1), prefix_len)
    If first_pile_prefix <> prefix Then
        MsgBox "请检查桩号前缀！"
        Exit Sub
    End If
    '循环所有行直到空行 line_index为行号
    Dim cur_pile_prefix As String
    Do While Cells(line_index, 1) <> ""
        cur_pile_prefix = Left(Cells(line_index, 1), prefix_len)                 '  取字符串Cells(j, 1)左边 S_LEN个字符
        '断面开始 此时line_index为桩号所在的行号
        If cur_pile_prefix = prefix Then                          '判断断面数据开始
            cur_pile = Cells(line_index, 1)
            cur_pile_m = ""
            cur_pile_km = ""                             '里程km
            Dim loop_index As Integer
            For loop_index = Len(cur_pile) To 1 Step -1
                If InStr("0123456789.", Mid(cur_pile, loop_index, 1)) Then '从单元格字符串的最末一个字符朝前开始判断是否为数字
                         cur_pile_m = Mid(cur_pile, loop_index, 1) & cur_pile_m$ '是数字，倒着存入变量cur_pile_m
                Else
                    Exit For
                End If
            Next loop_index
            For loop_index = prefix_len + 1 To Len(cur_pile) Step 1
                If InStr("0123456789", Mid(cur_pile, loop_index, 1)) Then '从单元格字符串的最末一个字符朝前开始判断是否为数字
                         cur_pile_km = cur_pile_km$ & Mid(cur_pile, loop_index, 1) '是数字，存入变量cur_pile_km
                Else
                    Exit For
                End If
            Next loop_index
            ar(3) = CDbl(cur_pile_km) * 1000 + CDbl(cur_pile_m)
            ar(15) = cur_pile         '桩号
            For loop_index = 1 To 21
                write_line_index = write_line_index + 1
                Cells(write_line_index, 4) = ar(loop_index - 1)
            Next loop_index
        Else
            write_line_index = write_line_index + 1
            Cells(write_line_index, 4) = Cells(line_index, 1)
            Cells(write_line_index, 5) = Cells(line_index, 2)
            Cells(write_line_index, 6) = zulixishu
        End If
        line_index = line_index + 1
    Loop
    Cells(write_line_index + 1, 4) = ar(0)
    '至此将表格除了mark之外的内容都写完
    Dim cur_line_index As Long
    cur_line_index = 1
    Dim mark
    mark = Array("<#0>", "<#1>", "<#2>", "<#3>", "<#4>", "<#5>", "<#6>", "<#7>")
    Do While Cells(cur_line_index, 4) <> ""
        Dim min As Double,l_max As Double,r_max As Double
        Dim total_point As Integer   '定义变量统计断面点数
        total_point = 0
        Dim point_num_line_index As Long     '定义变量确定点数写入的位置
        Dim cur_value As Variant
        Dim min_point_index As Long
        Dim l_max_point_index, r_max_point_index As Long
        '进入此if时，cur_line_index是数据的上一行
        If Cells(cur_line_index, 4) = ar(20) Then
            total_point = 0
            point_num_line_index = cur_line_index
            cur_line_index = cur_line_index + 1                      '断面数据第一点
            min = Cells(cur_line_index, 5)
            min_point_index = cur_line_index
            l_max = Cells(cur_line_index, 5)
            l_max_point_index = cur_line_index
            r_max = Cells(cur_line_index, 5)
            r_max_point_index = cur_line_index
            Do While (Cells(cur_line_index, 4) <> ar(0))    '统计一个断面的点数
               total_point = total_point + 1
               '开始重构算法
               cur_value = Cells(cur_line_index, 5).Value
                If (cur_value < min) Then
                    If (r_max > l_max) Then
                        l_max = r_max
                        l_max_point_index = r_max_point_index
                    End If
                    r_max = cur_value
                    r_max_point_index = cur_line_index
                    min = cur_value
                    min_point_index = cur_line_index
                Else
                    If (r_max < cur_value) Then
                        r_max = cur_value
                        r_max_point_index = cur_line_index
                    End If
                End If
                Cells(cur_line_index, 7) = mark(0)
                '结束重构算法
                cur_line_index = cur_line_index + 1
            Loop
            Cells(min_point_index, 7) = mark(2)
            Cells(l_max_point_index, 7) = mark(1)
            Cells(r_max_point_index, 7) = mark(4)
            Cells(point_num_line_index, 5) = total_point
        End If
        cur_line_index = cur_line_index + 1
    Loop
    Range("D1：H1").Select
    Selection.Delete Shift:=xlUp
 End Sub




