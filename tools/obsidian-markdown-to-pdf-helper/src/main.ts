import {FileSystemAdapter, MarkdownView, Notice, Plugin} from 'obsidian';
import {exec} from 'child_process';
import {DEFAULT_SETTINGS, MarkdownToPdfSettingTab, PluginSettings} from "./settings";

export default class MarkdownToPdfPlugin extends Plugin {
	settings: PluginSettings;

	async onload() {
		await this.loadSettings();

		this.addCommand({
			id: 'export-markdown-to-pdf',
			name: 'Export markdown to PDF',
			checkCallback: (checking: boolean) => {
				const markdownView = this.app.workspace.getActiveViewOfType(MarkdownView);
				if (!markdownView) return false;

				if (checking) return true;

				const activeFile = markdownView.file;
				if (!activeFile) {
					new Notice('No active file');
					return true;
				}

				this.exportToPdf(activeFile.path, activeFile.basename);
				return true;
			}
		});

		this.addSettingTab(new MarkdownToPdfSettingTab(this.app, this));
	}

	private exportToPdf(vaultRelativePath: string, basename: string): void {
		if (!this.settings.pythonToolPath) {
			new Notice('Please set the Python tool path in plugin settings');
			return;
		}
		if (!this.settings.exportFolder) {
			new Notice('Please set the export folder in plugin settings');
			return;
		}

		const adapter = this.app.vault.adapter as FileSystemAdapter;
		const basePath = adapter.getBasePath();
		const absolutePath = `${basePath}\\${vaultRelativePath}`;
		const outputPath = `${this.settings.exportFolder}\\${basename}.pdf`;
		const startBat = `${this.settings.pythonToolPath}\\start.bat`;
		const cmd = `"${startBat}" --input "${absolutePath}" --output "${outputPath}"`;

		console.log('[markdown-to-pdf] Running:', cmd);
		new Notice('Exporting to PDF...');

		exec(cmd, {cwd: this.settings.pythonToolPath}, (error, stdout, stderr) => {
			if (error) {
				const msg = stderr || error.message;
				console.error('[markdown-to-pdf] Failed:', msg);
				console.error('[markdown-to-pdf] stdout:', stdout);
				new Notice(`PDF export failed:\n${msg}`, 30000);
			} else {
				console.log('[markdown-to-pdf] Success:', outputPath);
				new Notice(`PDF exported: ${outputPath}`);
			}
		});
	}

	onunload() {}

	async loadSettings() {
		this.settings = Object.assign({}, DEFAULT_SETTINGS, await this.loadData() as Partial<PluginSettings>);
	}

	async saveSettings() {
		await this.saveData(this.settings);
	}
}
