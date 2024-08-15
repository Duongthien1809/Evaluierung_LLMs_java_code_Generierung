# import re
#
# def extract_generated_code(text):
#     if text is None:
#         return None
#
#     # This regex will match the entire block of Java code enclosed in triple backticks
#     match = re.search(r'```[\s\S]*?```', text, re.DOTALL)
#
#     if match:
#         # Remove the enclosing backticks
#         code_block = match.group(0)
#         code_block = code_block.strip('```')
#     else:
#         # If no backticks, use the entire text
#         code_block = text
#
#     # Find the package statement and return the code from there
#     package_index = code_block.find('package')
#     if package_index != -1:
#         code_block = code_block[package_index:]
#     else:
#         # If no package statement, search for import statement
#         import_index = code_block.find('import')
#         if import_index != -1:
#             code_block = code_block[import_index:]
#         else:
#             # If no import statement, search for public class statement
#             class_index = code_block.find('public class')
#             if class_index != -1:
#                 code_block = code_block[class_index:]
#
#     # Remove any text after the last closing brace
#     last_brace_index = code_block.rfind('}')
#     if last_brace_index != -1:
#         code_block = code_block[:last_brace_index + 1]
#
#     return code_block.strip()
#
# # Beispielhafte Verwendung
# generated_code = """
# Hier könnte etwas Text stehen.
# sdfdsfgsadfsd
#
# import java.ultil.*
# // #Medium #Array #Binary_Search #Binary_Search_II_Day_6
# // #2022_05_10_Time_86_ms_(88.58%)_Space_100.1_MB_(51.38%)
# public class Solution {
#     public int minSpeedOnTime(int[] dist, double hour) {
#         // Überprüfen, ob es möglich ist, rechtzeitig mit 1 km/h anzukommen
#         if (hour <= dist.length - 1) {
#             return -1;
#         }
#         // Initialisierung von Variablen für die binäre Suche
#         int left = 1;
#         int right = (int) 1e7;
#         int mid;
#         // Binäre Suche nach der minimalen Geschwindigkeit
#         while (left < right) {
#             mid = left + (right - left) / 2;
#             double time = getTime(dist, mid);
#             if (time <= hour) {
#                 right = mid;
#             } else {
#                 left = mid + 1;
#             }
#         }
#         // Überprüfen, ob es möglich ist, rechtzeitig mit der minimalen Geschwindigkeit anzukommen
#         double time = getTime(dist, left);
#         return time > hour ? -1 : left;
#     }
#
#     // Hilfsfunktion zur Berechnung der Gesamtzeit bei gegebener Geschwindigkeit
#     private double getTime(int[] dist, int speed) {
#         double time = 0;
#         for (int i = 0; i < dist.length - 1; i++) {
#             time += Math.ceil((double) dist[i] / speed);
#         }
#         time += (double) dist[dist.length - 1] / speed;
#         return time;
#     }
# }
#
# dsfdsfadsfadsf
# """
# print(extract_generated_code(generated_code))
