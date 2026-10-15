"""KiCad PCB Editor action plugin for the CPWG transition analyzer."""

try:
    import pcbnew
except ImportError:
    pcbnew = None


if pcbnew is not None:
    class ArchitectureBaseCPWGPlugin(pcbnew.ActionPlugin):
        def defaults(self):
            self.name = "Analyze CPWG Transition"
            self.category = "RF Tools"
            self.description = "Estimate impedance and reflection for a CPWG transition"
            self.show_toolbar_button = False

        def Run(self):
            import wx

            from rf_discontinuity_analyzer import analyze_transition

            dialog = wx.Dialog(None, title=self.name)
            fields = (
                ("Width before (mm)", "0.30"),
                ("Gap before (mm)", "0.20"),
                ("Width after (mm)", "0.25"),
                ("Gap after (mm)", "0.20"),
                ("Substrate relative permittivity", "4.2"),
            )
            controls = []
            layout = wx.FlexGridSizer(rows=len(fields), cols=2, hgap=8, vgap=8)
            layout.AddGrowableCol(1, 1)
            for label, default in fields:
                layout.Add(wx.StaticText(dialog, label=label), 0, wx.ALIGN_CENTER_VERTICAL)
                control = wx.TextCtrl(dialog, value=default)
                controls.append(control)
                layout.Add(control, 1, wx.EXPAND)

            outer = wx.BoxSizer(wx.VERTICAL)
            outer.Add(layout, 1, wx.ALL | wx.EXPAND, 12)
            outer.Add(dialog.CreateButtonSizer(wx.OK | wx.CANCEL), 0, wx.ALL | wx.EXPAND, 12)
            dialog.SetSizerAndFit(outer)

            if dialog.ShowModal() == wx.ID_OK:
                try:
                    values = [float(control.GetValue()) for control in controls]
                    result = analyze_transition(*values)
                except ValueError as error:
                    wx.MessageBox(str(error), self.name, wx.OK | wx.ICON_ERROR)
                else:
                    return_loss = (
                        "∞"
                        if result.return_loss_db == float("inf")
                        else f"{result.return_loss_db:.2f} dB"
                    )
                    message = (
                        f"Impedance before: {result.impedance_before_ohm:.2f} Ω\n"
                        f"Impedance after: {result.impedance_after_ohm:.2f} Ω\n"
                        f"Reflection coefficient: "
                        f"{result.reflection_coefficient:.4f}\n"
                        f"Return loss: {return_loss}\n"
                        f"VSWR: {result.vswr:.3f}"
                    )
                    wx.MessageBox(message, self.name, wx.OK | wx.ICON_INFORMATION)
            dialog.Destroy()


    ArchitectureBaseCPWGPlugin().register()
