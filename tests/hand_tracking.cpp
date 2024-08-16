#include <opencv2/opencv.hpp>
#include <mediapipe/framework/formats/landmark.pb.h>
#include <mediapipe/solutions/hands.h>
#include <mediapipe/solutions/drawing_utils.h>
#include <windows.h>

using namespace cv;
using namespace mediapipe;
using namespace std;

// Função para converter coordenadas de imagem para coordenadas de tela
POINT convertToScreenCoordinates(float x, float y, int screen_width, int screen_height, int safe_margin) {
    POINT pt;
    pt.x = screen_width - int(x * (screen_width - 2 * safe_margin)) + safe_margin;
    pt.y = int(y * (screen_height - 2 * safe_margin)) + safe_margin;
    return pt;
}

int main() {
    // Inicializar o video capture
    VideoCapture video(0);

    // Inicializar o MediaPipe Hands
    Hands hands;
    hands.Initialize();

    // Configurar a tela e a margem segura
    int screen_width = GetSystemMetrics(SM_CXSCREEN);
    int screen_height = GetSystemMetrics(SM_CYSCREEN);
    int safe_margin = 2;

    bool click_triggered = false;

    while (true) {
        Mat img;
        video >> img;
        if (img.empty()) break;

        // Converter imagem para RGB
        Mat imgRGB;
        cvtColor(img, imgRGB, COLOR_BGR2RGB);

        // Processar a imagem com o MediaPipe Hands
        std::vector<NormalizedLandmarkList> landmarks;
        hands.Process(imgRGB, landmarks);

        for (const auto& landmarks_list : landmarks) {
            // Desenhar os pontos das mãos
            for (const auto& landmark : landmarks_list.landmark()) {
                int cx = int(landmark.x() * img.cols);
                int cy = int(landmark.y() * img.rows);

                POINT screen_point = convertToScreenCoordinates(landmark.x(), landmark.y(), screen_width, screen_height, safe_margin);

                if (landmark.has_id() && landmark.id() == 9) {
                    // Mover o cursor do mouse
                    SetCursorPos(screen_point.x, screen_point.y);
                }

                // Verificar condição de clique
                bool click_condition = true;
                for (const auto& [d, b] : points_to_check) {
                    if (landmarks_list.landmark(d).y() <= landmarks_list.landmark(b).y()) {
                        click_condition = false;
                        break;
                    }
                }

                if (click_condition && !click_triggered) {
                    // Simular o clique do mouse
                    mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0);
                    mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0);
                    click_triggered = true;
                } else if (!click_condition) {
                    click_triggered = false;
                }
            }
        }

        // Mostrar a imagem
        imshow("Hand Tracking", img);
        if (waitKey(1) == 27) break; // Pressione ESC para sair
    }

    return 0;
}
