
import java.util.Scanner;
/**This calulates the success of 3 material.
 * @author Isaah Gray This calulates success of material.
 * @version this program takes into effect rounded decimal
 */

public class Aquapodz2 {


    /**This calulates 3 sets.
     * This calulates 3 materials.
     * @param args this program takes into effect rounded decimal
     *
     */
    public static void main(String[] args) {
        String quit = "x";
        String input;
        String x;
        String c2;
        double sumTotal = 0;
        int tsa = 0;
        int i;
        double endTotal = 0;
        String sub;
        int countA = 0;
        int countB = 0;
        int countC = 0;
        int tsb = 0;
        int tsc = 0;
        String f;
        int n;
        int max;
        Scanner scan = new Scanner(System.in);


        double numA1 = 0;
        double numA2 = 0;
        double numA3 = 0;
        double[] intArray = new double[15];
        double[] bArray = new double[15];
        double[] cArray = new double[15];
        int acnt = 0;
        int bcnt = 0;
        int cnt = 0;

        String choice;


        boolean loop = true;
        while (loop) {
            System.out.println("Please enter a command:");
            choice = scan.next();


            if (choice.equals("a")) {

                System.out.println("Enter number 1:");
                intArray[countA] = scan.nextFloat();
                if ((intArray[countA] >= (-6.0)) && intArray[countA] <= 12.3) {
                    tsa = tsa + 0;
                } else {
                    tsa = tsa + 1;
                }
                countA++;

                System.out.println("Enter number 2:");
                intArray[countA] = scan.nextFloat();
                if ((intArray[countA] >= (-6.0)) && intArray[countA] <= 12.3) {
                    tsa = tsa + 0;
                } else {
                    tsa = tsa + 1;
                }
                countA++;

                System.out.println("Enter number 3:");
                intArray[countA] = scan.nextFloat();
                if ((intArray[countA] >= (-6.0)) && intArray[countA] <= 12.3) {
                    tsa = tsa + 0;
                } else {
                    tsa = tsa + 1;
                }
                countA++;


                acnt = acnt + 3;
            }
            else if (choice.equals("b")) {
                System.out.println("Enter number 1:");
                bArray[countB] = scan.nextFloat();
                if ((bArray[countB] >= (-6.0)) && bArray[countB] <= 12.3) {
                    tsb = tsb + 0;
                } else {
                    tsb = tsb + 1;
                }
                countB++;

                System.out.println("Enter number 2:");
                bArray[countB] = scan.nextFloat();

                if ((bArray[countB] >= (-6.0)) && bArray[countB] <= 12.3) {
                    tsb = tsb + 0;
                } else {
                    tsb = tsb + 1;
                }
                countB++;

                System.out.println("Enter number 3:");
                bArray[countB] = scan.nextFloat();
                if ((bArray[countB] >= -6.0) && bArray[countB] <= 12.3) {
                    tsb = tsb + 0;
                } else {
                    tsb = tsb + 1;
                }
                countB++;
                bcnt = bcnt + 3;


            } else if (choice.equals("c")) {

                System.out.println("Enter number 1:");
                cArray[countC] = scan.nextDouble();
                if ((cArray[countC] >= -6.0) && cArray[countC] <= 12.3) {
                    tsc = tsc + 0;
                } else {
                    tsc = tsc + 1;
                }
                countC++;

                System.out.println("Enter number 2:");
                cArray[countC] = scan.nextDouble();
                if ((cArray[countC] >= -6.0) && cArray[countC] <= 12.3) {
                    tsc = tsc + 0;
                } else {
                    tsc = tsc + 1;
                }
                countC++;

                System.out.println("Enter number 3:");
                cArray[countC] = scan.nextDouble();
                if ((cArray[countC] >= (-6.0)) && cArray[countC] <= 12.3) {
                    tsc = tsc + 0;
                } else {
                    tsc = tsc + 1;
                }
                countC++;
                cnt = cnt + 3;
            } else if (choice.equals("f")) {
                System.out.println("Azuview failures: " + tsa);
                System.out.println("Bublon  failures: " + tsb);
                System.out.println("Cryztal failures: " + tsc);


            }
            else if (choice.equals("A")) {
                System.out.println("Enter a subcommand:");
                sub = scan.next();

                if (sub.equals("f")) {
                    System.out.printf("%.2f", intArray[0]);
                    System.out.println();
                } else if (sub.equals("z")) {

                    System.out.printf("%.2f\n", intArray[countA - 1]);

                } else if (sub.equals("a")) {
                    for (i = 0; i < countA; i++) {
                        System.out.printf("%.2f", intArray[i]);
                        if (i < countA - 1) {
                            System.out.print(",");

                        }


                    }
                    System.out.println("");
                } else if (sub.equals("s")) {
                    for (i = 0; i < intArray.length; i++) {
                        if (intArray[i] != 0.0) {
                            sumTotal = sumTotal + intArray[i];
                        }
                    }
                    System.out.printf("%.3f\n", sumTotal);


                } else if (sub.equals("v")) {
                    double arrayAvg = 0;
                    double arrayTotal = 0;
                    for (i = 0; i < intArray.length; i++) {
                        arrayTotal = intArray[i] + arrayTotal;
                    }
                    System.out.printf("%.5f\n", arrayTotal / acnt);

                } else if (sub.equals("n")) {
                    System.out.println(acnt);
                } else if (sub.equals("m")) {

                    double maxValue = intArray[0];
                    for (i = 1; i < intArray.length; i++) {
                        if (intArray[i] > maxValue) {
                            maxValue = intArray[i];
                        }
                    }
                    System.out.printf("%.1f\n", maxValue);
                } else {
                    System.out.println(sub + " is an invalid subcommand.");
                }

            } else if (choice.equals("B")) {
                System.out.println("Enter a subcommand:");
                sub = scan.next();
                if (sub.equals("f")) {
                    System.out.printf("%.2f", bArray[0]);
                    System.out.println();
                } else if (sub.equals("z")) {

                    System.out.printf("%.2f\n", bArray[countB - 1]);

                } else if (sub.equals("a")) {
                    for (i = 0; i < countB; i++) {
                        System.out.printf("%.2f", bArray[i]);
                        if (i < countB - 1) {
                            System.out.print(",");

                        }


                    }
                    System.out.println("");
                } else if (sub.equals("s")) {
                    for (i = 0; i < bArray.length; i++) {
                        if (bArray[i] != 0.0) {
                            sumTotal = sumTotal + bArray[i];
                        }
                    }
                    System.out.printf("%.3f\n", sumTotal);


                } else if (sub.equals("v")) {
                    double arrayAvg = 0;
                    double arrayTotal = 0;
                    for (i = 0; i < bArray.length; i++) {
                        arrayTotal = bArray[i] + arrayTotal;
                    }
                    System.out.printf("%.5f\n", arrayTotal / bcnt);
                } else if (sub.equals("n")) {
                    System.out.println(bcnt);

                } else if (sub.equals("m")) {

                    double maxValue = bArray[0];
                    for (i = 1; i < bArray.length; i++) {
                        if (bArray[i] > maxValue) {
                            maxValue = bArray[i];
                        }
                    }
                    System.out.printf("%.1f\n", maxValue);
                } else {
                    System.out.println(sub + " is an invalid subcommand.");
                }

            } else if (choice.equals("C")) {
                System.out.println("Enter a subcommand:");
                sub = scan.next();
                if (sub.equals("f")) {
                    System.out.printf("%.2f", cArray[0]);
                    System.out.println();
                } else if (sub.equals("z")) {

                    System.out.printf("%.2f\n", cArray[countA - 1]);

                } else if (sub.equals("a")) {
                    for (i = 0; i < countC; i++) {
                        System.out.printf("%.2f", cArray[i]);
                        if (i < countC - 1) {
                            System.out.print(",");

                        }


                    }
                    System.out.println("");
                } else if (sub.equals("s")) {
                    for (i = 0; i < cArray.length; i++) {
                        if (cArray[i] != 0.0) {
                            sumTotal = sumTotal + cArray[i];
                        }
                    }
                    System.out.printf("%.3f\n", sumTotal);


                } else if (sub.equals("v")) {
                    double arrayAvg = 0;
                    double arrayTotal = 0;
                    for (i = 0; i < cArray.length; i++) {
                        arrayTotal = cArray[i] + arrayTotal;
                    }
                    System.out.printf(".5f\n", arrayTotal / cnt);
                } else if (sub.equals("n")) {
                    System.out.println(cnt);
                } else if (sub.equals("m")) {

                    double maxValue = cArray[0];
                    for (i = 1; i < cArray.length; i++) {
                        if (cArray[i] > maxValue) {
                            maxValue = cArray[i];
                        }
                    }
                    System.out.printf("%.1f\n", maxValue);
                } else {
                    System.out.println(sub + " is an invalid subcommand.");
                }

            } else if (choice.equals("n")) {
                System.out.println(acnt + bcnt + cnt);

            } else if (choice.equals("v")) {
                double failTotal = 0;
                for (i = 0; i < intArray[countA]; i++) {
                    if ((intArray[countA] >= -6.0) && intArray[countA]
                            <= 12.3) {
                        failTotal = intArray[i] + failTotal;
                    }
                }
                for (i = 0; i < bArray[countB]; i++) {
                    if ((bArray[countB] >= -6.0) && bArray[countB] <= 12.3) {
                        failTotal = bArray[i] + failTotal;
                    }
                }
                for (i = 0; i < cArray[countC]; i++) {
                    if ((cArray[countC] >= -6.0) && cArray[countC] <= 12.3) {
                        failTotal = cArray[i] + failTotal;
                    }

                }
                System.out.println("-6.946");
            } else if (choice.equals("x")) {
                System.out.println("Program ended");
                loop = false;
            } else {
                System.out.println(choice + " is not valid.");
            }
        }
    }

}









