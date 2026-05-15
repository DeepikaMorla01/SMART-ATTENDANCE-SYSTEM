from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserIconView
# Import your AI functions
from attendance_scripts.mark_attendance import mark_attendance_from_image  

class AttendanceApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        self.label = Label(text="Select Classroom Image", size_hint=(1, 0.2))
        self.layout.add_widget(self.label)
        
        self.filechooser = FileChooserIconView(size_hint=(1, 0.6))
        self.layout.add_widget(self.filechooser)
        
        self.btn = Button(text="Mark Attendance", size_hint=(1, 0.2))
        self.btn.bind(on_press=self.mark_attendance)
        self.layout.add_widget(self.btn)
        
        return self.layout

    def mark_attendance(self, instance):
        selected = self.filechooser.selection
        if selected:
            image_path = selected[0]
            self.label.text = "Processing..."
            # Call your face recognition function here
            mark_attendance_from_image(image_path)  # Generates Excel
            self.label.text = "Attendance marked! Excel saved."
        else:
            self.label.text = "Please select an image."

if __name__ == "__main__":
    AttendanceApp().run()
